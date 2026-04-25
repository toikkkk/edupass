from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='StudentPredictionDataset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=150)),
                ('jurusan_sma', models.CharField(max_length=50)),
                ('nilai_sem1', models.DecimalField(decimal_places=2, max_digits=5)),
                ('nilai_sem2', models.DecimalField(decimal_places=2, max_digits=5)),
                ('nilai_sem3', models.DecimalField(decimal_places=2, max_digits=5)),
                ('nilai_sem4', models.DecimalField(decimal_places=2, max_digits=5)),
                ('nilai_sem5', models.DecimalField(decimal_places=2, max_digits=5)),
                ('rata_rata', models.DecimalField(decimal_places=2, max_digits=5)),
                ('nama_sekolah', models.CharField(db_index=True, max_length=255)),
                ('ranking', models.PositiveIntegerField(blank=True, db_index=True, null=True)),
                ('akreditasi', models.CharField(db_index=True, max_length=10)),
                ('indeks_sekolah', models.DecimalField(decimal_places=2, max_digits=6)),
                ('kuota_eligible', models.DecimalField(decimal_places=2, max_digits=4)),
                ('provinsi', models.CharField(db_index=True, max_length=100)),
                ('nilai_berbobot', models.DecimalField(decimal_places=2, max_digits=5)),
                ('target_ptn', models.CharField(db_index=True, max_length=255)),
                ('target_prodi', models.CharField(db_index=True, max_length=255)),
                ('target_jenjang', models.CharField(max_length=50)),
                ('passing_grade', models.DecimalField(decimal_places=2, max_digits=5)),
                ('daya_tampung_2026', models.PositiveIntegerField()),
                ('peminat_2025', models.PositiveIntegerField(blank=True, null=True)),
                ('rasio_keketatan', models.DecimalField(blank=True, decimal_places=4, max_digits=8, null=True)),
                ('target_lulus_snbp', models.BooleanField(db_index=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'student_prediction_datasets',
                'ordering': ['nama', 'target_ptn', 'target_prodi'],
            },
        ),
        migrations.AddIndex(
            model_name='studentpredictiondataset',
            index=models.Index(fields=['target_ptn'], name='student_pre_target__9de091_idx'),
        ),
        migrations.AddIndex(
            model_name='studentpredictiondataset',
            index=models.Index(fields=['target_prodi'], name='student_pre_target__0a77e7_idx'),
        ),
        migrations.AddIndex(
            model_name='studentpredictiondataset',
            index=models.Index(fields=['akreditasi'], name='student_pre_akredit_73c47d_idx'),
        ),
        migrations.AddIndex(
            model_name='studentpredictiondataset',
            index=models.Index(fields=['target_lulus_snbp'], name='student_pre_target__d22859_idx'),
        ),
    ]
