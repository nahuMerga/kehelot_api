# Generated by Django 5.1.6 on 2025-02-13 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kehelot_ai', '0002_remove_conversation_message_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='response',
            name='question',
        ),
        migrations.AddField(
            model_name='conversation',
            name='message',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='conversation',
            name='response',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Question',
        ),
        migrations.DeleteModel(
            name='Response',
        ),
    ]
