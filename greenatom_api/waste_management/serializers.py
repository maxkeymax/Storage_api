from rest_framework import serializers
from .models import Storage, Factory, FromFactoryToStorageDistance


class StorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Storage
        fields = '__all__'


class WasteDistributionSerializer(serializers.Serializer):
    plastic = serializers.IntegerField(min_value=0)
    glass = serializers.IntegerField(min_value=0)
    bio_waste = serializers.IntegerField(min_value=0)

    def validate(self, data):
        factory = self.context['factory']
        storages = Storage.objects.filter(storage_distances__factory=factory).order_by('storage_distances__distance')

        plastic = data['plastic']
        glass = data['glass']
        bio_waste = data['bio_waste']

        updated_storages = []

        for storage in storages:
            if plastic > 0:
                available_space = storage.plastic_max - storage.plastic_current
                if available_space > 0:
                    plastic_to_store = min(plastic, available_space)
                    storage.plastic_current += plastic_to_store
                    plastic -= plastic_to_store
                    updated_storages.append(storage)

            if glass > 0:
                available_space = storage.glass_max - storage.glass_current
                if available_space > 0:
                    glass_to_store = min(glass, available_space)
                    storage.glass_current += glass_to_store
                    glass -= glass_to_store
                    updated_storages.append(storage)

            if bio_waste > 0:
                available_space = storage.bio_waste_max - storage.bio_waste_current
                if available_space > 0:
                    bio_waste_to_store = min(bio_waste, available_space)
                    storage.bio_waste_current += bio_waste_to_store
                    bio_waste -= bio_waste_to_store
                    updated_storages.append(storage)

        if plastic > 0:
            raise serializers.ValidationError(f'Недостаточно места для всех пластиковых отходов. Следует уменьшить количество на {plastic}')
        if glass > 0:
            raise serializers.ValidationError(f'Недостаточно места для всех стекловых отходов. Следует уменьшить количество на {glass}')
        if bio_waste > 0:
            raise serializers.ValidationError(f'Недостаточно места для всех биологических отходов. Следует уменьшить количество на {bio_waste}')

        self._updated_storages = updated_storages
        return data

    def save(self):
        for storage in self._updated_storages:
            storage.save()