from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='PassingGrade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama_ptn', models.CharField(db_index=True, max_length=255)),
                ('akronim', models.CharField(blank=True, max_length=50, null=True)),
                ('nama_prodi', models.CharField(db_index=True, max_length=255)),
                ('jenjang', models.CharField(max_length=50)),
                ('nilai_rata_rata', models.DecimalField(decimal_places=2, max_digits=5)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'passing_grades',
                'ordering': ['nama_ptn', 'nama_prodi'],
            },
        ),
        migrations.CreateModel(
            name='Capacity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama_ptn', models.CharField(db_index=True, max_length=255)),
                ('kode_resmi', models.BigIntegerField(db_index=True)),
                ('kategori', models.CharField(db_index=True, max_length=100)),
                ('kode_prodi', models.BigIntegerField(unique=True)),
                ('nama_prodi', models.CharField(db_index=True, max_length=255)),
                ('jenjang', models.CharField(max_length=50)),
                ('daya_tampung_2026', models.PositiveIntegerField()),
                ('peminat_2025', models.PositiveIntegerField(blank=True, null=True)),
                ('portofolio', models.CharField(blank=True, max_length=100, null=True)),
                ('rasio_keketatan', models.DecimalField(blank=True, db_index=True, decimal_places=4, max_digits=8, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'capacities',
                'ordering': ['nama_ptn', 'nama_prodi'],
            },
        ),
        migrations.AddIndex(
            model_name='passinggrade',
            index=models.Index(fields=['nama_ptn'], name='passing_gra_nama_ptn_11e7ad_idx'),
        ),
        migrations.AddIndex(
            model_name='passinggrade',
            index=models.Index(fields=['nama_prodi'], name='passing_gra_nama_pr_507804_idx'),
        ),
        migrations.AddIndex(
            model_name='passinggrade',
            index=models.Index(fields=['nama_ptn', 'nama_prodi'], name='passing_gra_nama_ptn_1fdd54_idx'),
        ),
        migrations.AddConstraint(
            model_name='passinggrade',
            constraint=models.UniqueConstraint(fields=('nama_ptn', 'nama_prodi', 'jenjang'), name='uniq_passing_grade_ptn_prodi_jenjang'),
        ),
        migrations.AddIndex(
            model_name='capacity',
            index=models.Index(fields=['nama_ptn'], name='capacities_nama_ptn_9005ee_idx'),
        ),
        migrations.AddIndex(
            model_name='capacity',
            index=models.Index(fields=['nama_prodi'], name='capacities_nama_pr_39a0b3_idx'),
        ),
        migrations.AddIndex(
            model_name='capacity',
            index=models.Index(fields=['kategori'], name='capacities_kategori_232f7e_idx'),
        ),
        migrations.AddIndex(
            model_name='capacity',
            index=models.Index(fields=['rasio_keketatan'], name='capacities_rasio_k_e1976a_idx'),
        ),
    ]
