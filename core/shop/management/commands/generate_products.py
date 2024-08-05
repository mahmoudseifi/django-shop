from django.core.management.base import BaseCommand
from faker import Faker
from accounts.models import User, UserType
from django.utils.text import slugify
import random
from pathlib import Path
from django.core.files import File
from ...models import ProductModel, ProductCategoryModel, ProductStatusType

BASE_DIR = Path(__file__).resolve().parent

class Command(BaseCommand):
    help = 'Generate fake products'

    def handle(self, *args, **kwargs):
        fake = Faker(locale='fa_IR')
       
        user = User.objects.get(type=UserType.admin.value)
        categories = ProductCategoryModel.objects.all()  # Get all categories
        
        # list of images
        image_list = [
            './images/image_1.jpg',
            './images/image_2.jpg',
            './images/image_3.jpg',            
            './images/image_4.jpg', 
            './images/image_5.jpg', 
        ]
        
        for _ in range(10):  # Adjust number of products to create
            user=user
            num_categories = random.randint(1,4)
            selected_categoreis = random.sample(list(categories), num_categories)
            title = ' '.join([fake.word() for _ in range(1,3)])
            slug = slugify(title, allow_unicode=True)
            selected_image = random.choice(image_list)
            image_obj = File(file=open(BASE_DIR / selected_image,"rb"),name=Path(selected_image).name)
            description = fake.paragraph(nb_sentences=10)
            breif_description = fake.paragraph(nb_sentences=1)
            stock = random.randint(0, 100)
            status = random.choice(ProductStatusType.choices)[0]
            price = fake.random_int(min=1000, max=100000)
            discount_percent = random.randint(0, 50)

            product = ProductModel.objects.create(
                user=user,
                title=title,
                slug=slug,
                image=image_obj,
                description=description,
                breif_description=breif_description,
                stock=stock,
                status=status,
                price=price,
                discount_percent=discount_percent, 
            )
            product.category.set(selected_categoreis)

        self.stdout.write(self.style.SUCCESS('Successfully generated 10 fake products'))
