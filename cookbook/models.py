from django.db import models
from django.contrib.auth.models import User


class FoodCategory(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Food(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(FoodCategory, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Unit(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class RecipeCategory(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField('date created')
    servings = models.IntegerField(null=True, blank=True)
    prep_time = models.TimeField(null=True, blank=True)
    cook_time = models.TimeField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    directions = models.TextField(null=True, blank=True)
    profile_pic = models.ImageField(upload_to='recipes',
                                    default='recipes/recipe-default.png')
    thumbnail = models.ImageField(upload_to='thumbnails',
                                  default='recipes/recipe-default.png')

    main_ingredient = models.ForeignKey(Food, null=True, on_delete=models.PROTECT, blank=True)

    def __str__(self):
        return self.name

    def create_thumbnail(self):
        if not self.profile_pic:
            return

        if self.thumbnail:
            if self.thumbnail.name.split(".")[0] == self.profile_pic.name.split(".")[0]+"_thumbnail":
                return

        from PIL import Image
        from io import BytesIO
        from django.core.files.uploadedfile import SimpleUploadedFile
        import os

        # max thumbnail size
        basewidth = 700

        if self.profile_pic.name.endswith(".jpg"):
            PIL_TYPE = 'jpeg'
            FILE_EXTENSION = 'jpg'

        elif self.profile_pic.name.endswith(".png"):
            PIL_TYPE = 'png'
            FILE_EXTENSION = 'png'
        else:
            PIL_TYPE = 'png'
            FILE_EXTENSION = 'png'

        try:
            image = Image.open(self.profile_pic)
        except:
            return
        wpercent = (basewidth/float(image.size[0]))
        hsize = int((float(image.size[1])*float(wpercent)))
        image.thumbnail((basewidth, hsize), Image.ANTIALIAS)

        temp_handle = BytesIO()
        image.save(temp_handle, PIL_TYPE)
        temp_handle.seek(0)

        # Save image to a SimpleUploadedFile which can be saved into
        # ImageField
        suf = SimpleUploadedFile(os.path.split(self.profile_pic.name)[-1],
                                 temp_handle.read(), content_type="image/"+PIL_TYPE)
        # Save SimpleUploadedFile into image field
        self.thumbnail.save(
            '%s_thumbnail.%s' % (os.path.splitext(suf.name)[0], FILE_EXTENSION),
            suf,
            save=False
        )

    def save(self, *args, **kwargs):

        self.create_thumbnail()

        force_update = False

        # If the instance already has been saved, it has an id and we set
        # force_update to True
        if self.id:
            force_update = True

        # Force an UPDATE SQL query if we're editing the image to avoid integrity exception
        super(Recipe, self).save(force_update=force_update)


class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.PROTECT)
    amount = models.FloatField(null=False)
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.amount) + " " + str(self.unit) + " of " + str(self.food)


class Menu(models.Model):
    week_of = models.DateField('date created')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipes = models.ManyToManyField('Recipe')

    def __str__(self):
        return "Week of: " + str(self.week_of)