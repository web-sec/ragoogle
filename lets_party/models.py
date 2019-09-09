import re
import logging

from django.db import models
from django.urls import reverse

from abstract.models import AbstractDataset
from abstract.tools.companies import generate_edrpou_options
from abstract.ftm_models import model as ftm_model
from abstract.tools.ftm import person_entity, company_entity
from names_translator.name_utils import (
    parse_and_generate,
    autocomplete_suggestions,
    generate_all_names,
)


logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("LetsParty")


class LetsPartyModel(AbstractDataset):
    TYPES = {
        "nacp": "Звіти партій до НАЗК",
        "parliament": "Звіти парламентських виборів до ЦВК",
        "president": "Звіти президентських виборів до ЦВК",
    }
    type = models.CharField("Джерело даних", max_length=20, choices=TYPES.items())
    period = models.CharField("Період звіту", max_length=30)
    ultimate_recepient = models.CharField(
        "Кінцевий отримувач коштів", max_length=255, db_index=True
    )

    def get_absolute_url(self):
        return reverse("LetsParty>details", kwargs={"pk": self.id})

    def to_dict(self):
        dt = self.data
        res = {"_id": self.pk}

        names_autocomplete = set()
        companies = (
            set([dt["party"]])
            | generate_edrpou_options(dt["donator_code"])
            | generate_edrpou_options(dt["party"])
        )

        if dt.get("branch_code"):
            companies |= generate_edrpou_options(dt["branch_code"])

        if dt.get("branch_name"):
            companies |= generate_edrpou_options(dt["branch_name"])

        addresses = set([dt["donator_location"]])
        persons = set([dt.get("candidate_name")])

        if dt["donator_code"]:
            companies |= set([dt["donator_name"]])
        else:
            persons |= parse_and_generate(dt["donator_name"], "Донор")
            names_autocomplete |= autocomplete_suggestions(dt["donator_name"])

        names_autocomplete |= companies
        raw_records = set(
            [
                dt.get("account_number"),
                dt.get("payment_subject"),
                dt["transaction_doc_number"],
            ]
        )

        res.update(dt)
        res.update(
            {
                "companies": list(filter(None, companies)),
                "addresses": list(filter(None, addresses)),
                "persons": list(filter(None, persons)),
                "names_autocomplete": list(filter(None, names_autocomplete)),
                "raw_records": list(filter(None, raw_records)),
                "type": self.get_type_display(),
                "period": self.period,
                "ultimate_recepient": self.ultimate_recepient,
            }
        )

        return res

    def to_entities(self):
        dt = self.data

        if dt["donator_code"]:
            donor = company_entity(
                dt["donator_name"],
                dt["donator_code"],
                id_prefix=self.ultimate_recepient,
                address=dt["donator_location"],
            )
        else:
            donor = person_entity(
                dt["donator_name"],
                "Донор",
                id_prefix=self.pk,
                address=dt["donator_location"],
            )

        donor.set(
            "description",
            "{}, {} зробила пожертву у розмірі {} гривень на {} {}".format(
                dt["donator_type"],
                dt["donation_date"],
                dt["amount"],
                "партію"
                if self.type in ["nacp", "parliament"]
                else "кандидата в президенти",
                self.ultimate_recepient,
            ),
        )
        yield donor

        if self.type in ["nacp", "parliament"]:
            if dt.get("branch_code"):
                beneficiary = company_entity(
                    "{}, {}".format(dt["party"], dt["branch_name"]),
                    dt["branch_code"],
                    id_prefix=self.ultimate_recepient,
                    address=dt.get("geo"),
                )
            else:
                beneficiary = company_entity(
                    dt["party"],
                    dt["party"],
                    id_prefix=self.ultimate_recepient,
                    address=dt.get("geo"),
                )
        else:
            beneficiary = person_entity(
                dt["candidate_name"],
                "Кандидат в президенти, {}".format(dt["party"]),
                id_prefix=self.ultimate_recepient,
            )


        beneficiary.set(
            "description",
            "{} отримав пожертву у розмірі {} гривень від {} ({})".format(
                dt["donation_date"],
                dt["amount"],
                dt["donator_name"],
                dt["donator_type"],
            ),
        )

        yield beneficiary

        if dt.get("party", "cамовисування").lower() != "cамовисування" and dt.get("branch_code"):
            party = company_entity(
                dt["party"],
                dt["party"],
                id_prefix=self.ultimate_recepient,
            )
            yield party

            directorship = ftm_model.make_entity("Directorship")
            directorship.make_id(dt["party"], dt["branch_code"], "party")

            directorship.add("director", party.id)
            directorship.add("organization", beneficiary)
            directorship.add("role", "Головний офіс")
            yield directorship

        if dt.get("bank_name", "") and dt.get("account_number", ""):
            account = ftm_model.make_entity("BankAccount")
            account.make_id(dt["account_number"], "account")
            if dt.get("bank_name", ""):
                account.add("bankName", dt["bank_name"])

            if dt.get("account_number", ""):
                account.add("accountNumber", dt["account_number"])

            yield account
        else:
            account = None

        donation = ftm_model.make_entity("RingDonation")
        if dt.get("payment_subject"):
            donation.add("purpose", dt["payment_subject"])

        donation.add("payer", donor.id)
        donation.add("beneficiary", beneficiary.id)
        donation.add("amount", dt["amount"])
        donation.add("currency", "UAH")

        if account is not None:
            donation.add("beneficiaryAccount", account.id)

        donation.make_id(self.pk, "donation")
        yield donation
