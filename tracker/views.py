from rest_framework import generics, permissions, viewsets
from rest_framework.exceptions import PermissionDenied
from .models import User, MiniProject
from .serializers import UserSerializer, MiniProjectSerializer


# 🔹 User Registration
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


# 🔹 MiniProject list + create (role-based logic)
class MiniProjectListCreateView(generics.ListCreateAPIView):
    serializer_class = MiniProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == "trainer":
            return MiniProject.objects.filter(trainer=user).order_by("-id")
        return MiniProject.objects.filter(trainee=user).order_by("-id")

    def perform_create(self, serializer):
        if self.request.user.role != "trainer":
            raise PermissionDenied("Only trainers can create projects.")
        serializer.save(trainer=self.request.user)


# 🔹 MiniProject update (trainer only)
class MiniProjectUpdateView(generics.UpdateAPIView):
    serializer_class = MiniProjectSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "pk"

    def get_queryset(self):
        user = self.request.user
        if user.role != "trainer":
            raise PermissionDenied("Only trainers can update projects.")
        return MiniProject.objects.filter(trainer=user)

    def perform_update(self, serializer):
        serializer.save()


# =============================
# ✅ Extra: Read-only endpoints for DRF UI browsing
# =============================

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """View all users (admin/testing only)"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]  # set to IsAdminUser if you want to restrict


class MiniProjectViewSet(viewsets.ReadOnlyModelViewSet):
    """View all projects (admin/testing only)"""
    queryset = MiniProject.objects.all()
    serializer_class = MiniProjectSerializer
    permission_classes = [permissions.AllowAny]  # set to IsAuthenticated if you want to restrict
