from django.db import models

# Create your models here.
class Provider(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    contact_phone = models.CharField(max_length=50, null=True, blank=True)
    contact_email = models.EmailField(null=True, blank=True)
    contact_address = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
    
class Availability(models.Model):
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.start_date} - {self.end_date}: {self.status}"
    
class Equipment(models.Model):
    name = models.CharField(max_length=255)
    Type = models.CharField(max_length=255, null=True, blank=True)
    brand = models.CharField(max_length=255,null=False, default="Unknown")
    model = models.CharField(max_length=255,null=False, default="Unknown")
    resolution = models.CharField(max_length=50, null=True, blank=True)
    frame_rate = models.CharField(max_length=50, null=True, blank=True)
    sensor_type = models.CharField(max_length=50, null=True, blank=True)
    connectivity = models.JSONField(null=True, blank=True)
    audio_input = models.JSONField(null=True, blank=True)
    battery_life = models.CharField(max_length=50, null=True, blank=True)
    weight = models.CharField(max_length=50, null=True, blank=True)
    accessories = models.JSONField(null=True, blank=True)
    rental_price_per_day = models.CharField(max_length=50, null=True, blank=True)
    # provider = models.ManyToManyField(Provider)
    # availability = models.ManyToManyField(Availability)
    provider = models.CharField(max_length=50, null=True, blank=True)
    availability = models.CharField(max_length=50, null=True, blank=True)
    height_range = models.CharField(max_length=50, null=True, blank=True)
    weight_capacity = models.CharField(max_length=50, null=True, blank=True)
    material = models.CharField(max_length=50, null=True, blank=True)
    inputs = models.JSONField(null=True, blank=True)
    output = models.CharField(max_length=50, null=True, blank=True)
    resolution_support = models.CharField(max_length=50, null=True, blank=True)
    control_interface = models.CharField(max_length=50, null=True, blank=True)
    wireless = models.CharField(max_length=50, null=True, blank=True)
    frequency_range = models.CharField(max_length=50, null=True, blank=True)
    frequency_response = models.CharField(max_length=50, null=True, blank=True)
    transmitter_battery_life = models.CharField(max_length=50, null=True, blank=True)
    transducer_type = models.CharField(max_length=50, null=True, blank=True)
    directionality = models.CharField(max_length=50, null=True, blank=True)
    channels = models.CharField(max_length=50, null=True, blank=True)
    effects = models.CharField(max_length=50, null=True, blank=True)
    speaker_type = models.CharField(max_length=50, null=True, blank=True)
    power_rating = models.CharField(max_length=50, null=True, blank=True)
    light_type = models.CharField(max_length=50, null=True, blank=True)
    power = models.CharField(max_length=50, null=True, blank=True)
    color_temperature = models.CharField(max_length=50, null=True, blank=True)
    brightness = models.CharField(max_length=50, null=True, blank=True)
    dimensions = models.CharField(max_length=50, null=True, blank=True)
    shape = models.CharField(max_length=50, null=True, blank=True)
    diffuser_type = models.CharField(max_length=50, null=True, blank=True)
    mount_type = models.CharField(max_length=50, null=True, blank=True)
    sections = models.CharField(max_length=50, null=True, blank=True)
    features = models.CharField(max_length=50, null=True, blank=True)
    speed = models.CharField(max_length=50, null=True, blank=True)
    cable_type = models.CharField(max_length=50, null=True, blank=True)
    length = models.CharField(max_length=50, null=True, blank=True)
    bandwidth = models.CharField(max_length=50, null=True, blank=True)
    range = models.CharField(max_length=50, null=True, blank=True)
    screen_size = models.CharField(max_length=50, null=True, blank=True)
    compatibility = models.CharField(max_length=50, null=True, blank=True)
    processor = models.CharField(max_length=50, null=True, blank=True)
    memory = models.CharField(max_length=50, null=True, blank=True)
    storage = models.CharField(max_length=50, null=True, blank=True)
    power_capacity = models.CharField(max_length=50, null=True, blank=True)
    battery_runtime = models.CharField(max_length=50, null=True, blank=True)
    graphics_card = models.CharField(max_length=50, null=True, blank=True)
    license_type = models.CharField(max_length=50, null=True, blank=True)
    media_support = models.CharField(max_length=50, null=True, blank=True)
    interface = models.CharField(max_length=50, null=True, blank=True)
    capacity = models.CharField(max_length=50, null=True, blank=True)
    load_capacity = models.CharField(max_length=50, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name

class EquipmentRequirement(models.Model):
    project = models.ForeignKey('project.Project', on_delete=models.CASCADE, related_name='equipment_requirements_set')
    name = models.CharField(max_length=50)
    Specification_required = models.TextField(default="")
    location = models.CharField(max_length=50)
    number_needed = models.IntegerField()
    
    def __str__(self):
        return self.name

class SelectedEquipments(models.Model):
    project = models.ForeignKey('project.Project', on_delete=models.CASCADE, related_name='selected_equipment_set')
    equipment = models.ForeignKey('Equipment', on_delete=models.CASCADE)
    equipment_requirements = models.ForeignKey('EquipmentRequirement', on_delete=models.CASCADE)
    preferred_because = models.TextField(default="Did not store the field") #remove this after deleting previous data
    
    def __str__(self):
        return self.equipment.name


