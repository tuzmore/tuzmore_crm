from rest_framework import generics, permissions, viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer, UserSerializer, AdminCreateUserSerializer
from .permissions import IsAdmin, IsManager, IsSales
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .utils import account_activation_token


User = get_user_model()

# Email 
def send_verfication_email(request, user):
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    token = account_activation_token.make_token(user)
    # build absolute URL
    activation_path = reverse('users:activate', 
        kwargs={'uidb64': uidb64, 'token': token })
    activation_link = request.build_absolute_uri(activation_path)
    subject = 'Verify your Tuzmore account'
    message = f'Hi {user.username}, \n\nPlease verify your account by clicking the link:\n{activation_link}\n\nIf you did not register, ignore this email.'
    send_mail(subject, message, None, [user.email], fail_silently=False)

# Public registration endpoint
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        user = serializer.save(is_active=False, is_verified=False)




# Admin-only user list / create (if you want an admin endpoint)
class AdminUserViewSet(viewsets.ModelViewSet):
    """
    Admin-only user management. Use AdminCreateUserSerializer to allow role set.
    """
    queryset = User.objects.all().order_by("-id")
    permission_classes = [IsAdmin]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return AdminCreateUserSerializer
        return UserSerializer


# Simple role-based test endpoints (optional)
@api_view(["GET"])
@permission_classes([IsManager])
def manager_dashboard(request):
    return Response({"message": "Welcome Manager! you can view reports here."})


@api_view(["GET"])
@permission_classes([IsSales])
def sales_dashboard(request):
    return Response({"message": "Welcome Sales! you can view your leads here."})

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def activate_user(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception:
        user = None

    if user and account_activation_token.check_token(user, token):
        user.is_active = True
        user.is_verified = True
        user.save()
        # you can redirect to a success page or return JSON
        return Response({'detail': 'Email verified successfully.'})
    return Response({'detail': 'Invalid or expired token.'}, status=400)