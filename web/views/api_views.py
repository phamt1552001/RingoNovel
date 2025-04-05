from rest_framework import viewsets, status
from rest_framework.response import Response

from ..models import Novel
from ..serializers import NovelSerializers

class API_NovelViewSet(viewsets.ModelViewSet):
    queryset = Novel.objects.all()
    serializer_class = NovelSerializers
    # authentication_classes = [JWTAuthentication]  # Bắt buộc dùng JWT để xác thực
    # permission_classes = [IsAuthenticated]  # Chỉ cho phép user đã đăng nhập truy cập
    
    def update(self, request, *args, **kwargs):
        novel = self.get_object()
        if novel.author != request.user or request.user.is_staff :  # Chỉ cho tác giả sửa
            return Response({'error': 'Bạn không phải tác giả của truyện này!'}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        novel = self.get_object()
        if novel.author != request.user:  # Chỉ cho tác giả xóa
            return Response({'error': 'Bạn không có quyền xóa truyện này!'}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)
    
    
