# Generated by Django 2.2.4 on 2019-09-12 18:39

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lets_party', '0005_auto_20190902_0123'),
    ]

    operations = [
        migrations.CreateModel(
            name='LetsPartyRedFlag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flag_type', models.CharField(choices=[('suspicious', 'Suspicious'), ('violation', 'Violation')], max_length=20)),
                ('rule', models.CharField(choices=[('company_won_procurement', 'Компанія виграла у держзакупівлях'), ('company_had_tax_debts', 'Компанія мала держборг')], max_length=100)),
                ('related_entity', models.CharField(blank=True, max_length=100, verbose_name='Запис')),
                ('related_entity_source', models.CharField(choices=[('smida', 'Власники значної частки СМІДА'), ('posipaky_info', 'Помічники народних депутатів'), ('posipaky_2_info', 'Помічники місцевих депутатів'), ('edrdr', 'Єдиний державний реєстр юросіб (ЄДР)'), ('garnahata_in_ua', 'Реєстр власників елітної нерухомості'), ('vkks', "Декларації родинних зв'язків суддів та кандидатів"), ('nacp_declarations', 'Електронні декларації'), ('paper_declarations', 'Паперові декларації'), ('cvk_2015', 'Учасники місцевих виборів 2015-го року'), ('smida_reports', 'Звіти акціонерних товариств СМІДА'), ('dabi_licenses', 'Ліцензії ДАБІ'), ('dabi_registry', 'Реєстр дозволів ДАБІ'), ('geoinf_licenses', 'Ліцензії ДП Геоінформ'), ('mbu', 'Містобудівні умови м. Києва'), ('company_house_ua', 'Британський реєстр компаній'), ('tax_debts', 'Податковий борг'), ('procurement_winners', 'Переможці в закупівлях'), ('lets_party', 'Фінансові звіти партій та кандидатів'), ('corrupt', 'Особи, засуджені за корупцію')], max_length=50, verbose_name='Ідентифікатор датасету')),
                ('description', models.TextField(verbose_name='Текстовий опис червоного прапорця')),
                ('payload', django.contrib.postgres.fields.jsonb.JSONField(null=True, verbose_name='Додаткові відомості')),
                ('transaction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lets_party.LetsPartyModel')),
            ],
        ),
    ]