from django.db import migrations


def create_test_model_data(apps, schema_editor):
    TestModel = apps.get_model("labs", "TestModel")
    TestModel.objects.create(name="Test")
    TestModel.objects.create(name="Test 1")
    TestModel.objects.create(name="Test 2")
    TestModel.objects.create(name="Test 3")


def rollback(apps, schema_editor):
    TestModel = apps.get_model("labs", "TestModel")
    TestModel.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ("labs", "0004_testmodel"),
    ]

    operations = [
        migrations.RunPython(create_test_model_data, rollback),
    ]
