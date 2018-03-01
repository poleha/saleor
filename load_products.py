import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "saleor.settings")
from django.core.management import execute_from_command_line

execute_from_command_line(sys.argv)

from saleor.product.models import Product, Category, ProductImage, ProductClass, ProductVariant

product_class = ProductClass.objects.first()

import csv
Product.objects.all().delete()
ProductImage.objects.all().delete()
ProductVariant.objects.all().delete()
with open('products.csv', 'r') as f:
    reader = csv.DictReader(f, delimiter='|')
    next(reader)
    for line in reader:
        for k, v in line.items():
            line[k] = v.strip()
        price = line['price'].replace(',', '').replace('.00','')
        product, created = Product.objects.get_or_create(
            name=line['name'],
            product_class=product_class,
            description=line['description'],
            price=price,
        )
        try:
            category = Category.objects.get(name=line['category'])
            product.categories.set([category])
        except Exception as e:
            print(line['category'])
            product.delete()
            continue

        ProductVariant.objects.update_or_create(product=product, defaults={'sku': line['image']})
        images_path = os.path.join('load', 'images', line['image'])
        image_names = os.listdir(images_path)
        for image_name in image_names:
            product_image = ProductImage.objects.create(product=product)
            image_path = os.path.join(images_path, image_name)
            with open(image_path, 'rb') as image_file:
                product_image.image.save(image_name, image_file)



