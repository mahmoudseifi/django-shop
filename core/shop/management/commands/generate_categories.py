from django.core.management.base import BaseCommand
from faker import Faker
from django.utils.text import slugify
from ...models import ProductCategoryModel

class Command(BaseCommand):
    help = 'Generate fake product categories'

    def handle(self, *args, **kwargs):
        fake = Faker(locale='fa_IR')
        for _ in range(10):  # Generate 10 fake categories
            title = fake.unique.word()
            slug = slugify(title, allow_unicode=True)

            category = ProductCategoryModel.objects.get_or_create(
                title=title,
                slug=slug,
            )
        self.stdout.write(self.style.SUCCESS(f'Category "{title}" created.'))