from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Storer',
            fields=[
                ('doc_id', models.CharField(max_length=11, primary_key=True, serialize=False)),
                ('original_author_id', models.IntegerField(default='', null=True)),
                ('answers', models.JSONField()),
                ('contains_error', models.BooleanField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('editor_id', models.IntegerField(null=True)),
                ('feedback', models.JSONField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('score', models.IntegerField(null=True)),
                ('doc_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='feedback_doc_id', to='hypatia.storer')),
                ('original_author_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feedback_author_id', to='hypatia.storer')),
            ],
        ),
    ]
