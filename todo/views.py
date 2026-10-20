from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from .models import Todo
from .serializers import TodoSerializer
from .utils import api_response


class TodoViewSet(viewsets.ModelViewSet):
    serializer_class = TodoSerializer
    permission_classes = [IsAuthenticated]

    filterset_fields = ['is_completed', 'priority']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'due_date', 'priority']
    ordering = ['-created_at']

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user, is_deleted=False)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # CREATE
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return api_response(
            success=True,
            message="Todo created successfully",
            data=serializer.data,
            status_code=status.HTTP_201_CREATED
        )

    # LIST
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_data = self.paginator.get_paginated_response(serializer.data).data

            return api_response(
                success=True,
                message="Todos retrieved successfully",
                data=paginated_data,
                status_code=status.HTTP_200_OK
            )

        serializer = self.get_serializer(queryset, many=True)
        return api_response(
            success=True,
            message="Todos retrieved successfully",
            data=serializer.data,
            status_code=status.HTTP_200_OK
        )

    # RETRIEVE (Single Todo)
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        return api_response(
            success=True,
            message="Todo retrieved successfully",
            data=serializer.data,
            status_code=status.HTTP_200_OK
        )

    # UPDATE (PUT)
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return api_response(
            success=True,
            message="Todo updated successfully",
            data=serializer.data,
            status_code=status.HTTP_200_OK
        )

    # PARTIAL UPDATE (PATCH)
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    # DELETE (Soft Delete)
    def destroy(self, request, *args, **kwargs):
        todo = self.get_object()
        todo.is_deleted = True
        todo.save()

        return api_response(
            success=True,
            message="Todo deleted successfully",
            data=None,
            status_code=status.HTTP_200_OK
        )