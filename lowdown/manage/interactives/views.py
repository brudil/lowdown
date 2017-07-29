from rest_framework.authentication import TokenAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from lowdown.core.interactives.models import Interactive, InteractiveRelease
from .serializers import InteractiveSerializer, InteractiveReleaseSerializer
from rest_framework import generics


class ListCreateInteractives(generics.ListCreateAPIView):
    serializer_class = InteractiveSerializer
    queryset = Interactive.objects.all()


class ListCreateInteractiveReleases(generics.ListCreateAPIView):
    serializer_class = InteractiveReleaseSerializer
    queryset = InteractiveRelease.objects.all()
    authentication_classes = [JSONWebTokenAuthentication, TokenAuthentication]

    def get_queryset(self):
        queryset = super().get_queryset()

        slugs = self.request.query_params.getlist('slugs[]')
        if len(slugs) > 0:
            return queryset.filter(slugs__in=slugs)

        return queryset

    def perform_create(self, serializer):
        interactive, created = Interactive.objects.get_or_create(slug=self.kwargs['slug'])

        interactive.revision_count += 1

        serializer.save(interactive=interactive, revision_number=interactive.revision_count)

        interactive.save()


class RetrieveUpdateDestroyInteractives(generics.RetrieveUpdateDestroyAPIView):
    queryset = Interactive.objects.all()
    serializer_class = InteractiveSerializer
    authentication_classes = [JSONWebTokenAuthentication, TokenAuthentication]

    def perform_destroy(self, instance):
        instance.deleted = True
        instance.save()


class UpdateInteractiveRelease(generics.UpdateAPIView):
    serializer_class = InteractiveReleaseSerializer
    authentication_classes = [JSONWebTokenAuthentication, TokenAuthentication]

    def get_object(self):
        return InteractiveRelease.objects.get(
            interactive__slug=self.kwargs['slug'],
            revision_number=self.kwargs['rid']
        )
