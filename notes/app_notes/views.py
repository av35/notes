# Create your views here.
import json

from django.http import JsonResponse
from rest_framework.generics import get_object_or_404

from django.core import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Note


class MyApiView(APIView):
    def get(self, request, pk=None):
        if pk:
            note = Note.objects.filter(pk=pk)
            data = serializers.serialize('json', note)
            return JsonResponse(json.loads(data), safe=False)
        context = Note.objects.all()
        data = serializers.serialize('json', context)
        return JsonResponse(json.loads(data), safe=False)


    def post(self, request):
        # Create an article from the above data
        note = Note.objects.create(event=request.data.get('event'), when=request.data.get('when'))
        note.save()
        return Response({"success": "Note '{}' created successfully".format(note.pk)})


    def put(self, request, pk):
        # Create an article from the above data
        note = Note.objects.filter(pk=pk)
        data = serializers.serialize('json', note)
        str = json.loads(json.dumps(json.loads(data)[0]))
        values = {}

        if str['fields']['event'] != request.data.get('event'):
            values['event'] = request.data.get('event')

        if str['fields']['when'] != request.data.get('when'):
            values['when'] = request.data.get('when')

        note.update(**values)
        return Response({"success": "Note with id '{}' updated successfully".format(pk)})


    def delete(self, request, pk):
        # Get object with this pk
        note = get_object_or_404(Note.objects.all(), pk=pk)
        note.delete()
        return Response({"message": "Note with id '{}' has been deleted.".format(pk)},status=204)
