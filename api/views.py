from rest_framework import viewsets
from . import models
from . import serializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
    
# Registration ViewSets
class StudentRegistrationViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.StudentCustomRegistrationSerializer
    queryset = models.Student.objects.all()
    http_method_names = ['post']
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        student = serializer.save()
        student_data = serializers.StudentSerializer(student, context=self.get_serializer_context()).data
        
        return Response(
            {'student': student_data}, 
            status=status.HTTP_201_CREATED
        )

class StaffRegistrationViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.StaffCustomRegistrationSerializer
    queryset = models.Staff.objects.all()
    http_method_names = ['post']
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        staff = serializer.save()
        staff_data = serializers.StaffSerializer(staff, context=self.get_serializer_context()).data
        
        return Response(
            {'staff': staff_data},
            status=status.HTTP_201_CREATED
        )

class TechnicianRegistrationViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.TechnicianCustomRegistrationSerializer
    queryset = models.Technician.objects.all()
    http_method_names = ['post']
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        technician = serializer.save()
        technician_data = serializers.TechnicianSerializer(technician, context=self.get_serializer_context()).data
        
        return Response(
            {'technician': technician_data},
            status=status.HTTP_201_CREATED
        )

class AdminRegistrationViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.AdminCustomRegistrationSerializer
    queryset = models.Admin.objects.all()
    http_method_names = ['post']
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        admin = serializer.save()
        admin_data = serializers.AdminSerializer(admin, context=self.get_serializer_context()).data
        
        return Response(
            {'admin': admin_data},
            status=status.HTTP_201_CREATED
        )

class ChefRegistrationViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ChefCustomRegistrationSerializer
    queryset = models.Chef.objects.all()
    http_method_names = ['post']
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        chef = serializer.save()
        chef_data = serializers.ChefSerializer(chef, context=self.get_serializer_context()).data
        
        return Response(
            {"chef": chef_data},
            status=status.HTTP_201_CREATED
        )

# General ViewSets
class StudentViewSet(viewsets.ModelViewSet):
    queryset = models.Student.objects.all()
    serializer_class = serializers.StudentSerializer
    http_method_names = ['get', 'patch']    

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.StudentSerializer
        if self.request.method == 'PATCH':
            return serializers.StudentPatchSerializer
        return serializers.StudentSerializer

    def get_queryset(self):
        if self.request.method == 'GET':
            students = models.Student.objects.all()
            without_room = self.request.GET.get('without_room', None)
            order_students_by = self.request.GET.get('order_students_by', None)

            if without_room == 'true' or without_room == 'True':
                without_room = True
            elif without_room == 'false' or without_room == 'False':
                without_room = False
            else:
                without_room = ' '

            if without_room == True or without_room == False:
                students = students.filter(room__isnull=without_room)
            
            if order_students_by in [f.name for f in models.Student._meta.fields]:
                students = students.order_by(order_students_by)

            return students

        return models.Student.objects.all()

    @action(detail=True, methods=['get'])
    def room(self, request, pk=None):
        try: 
            room = models.Room.objects.get(student_id=pk)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.RoomSerializer(room, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def maintreqs(self, request, pk=None):
        reqs = models.MaintenanceRequest.objects.filter(student_id=pk)
        resolved = request.GET.get('resolved', None)
        order_reqs_by = request.GET.get('order_reqs_by', None)

        if resolved == 'true' or resolved == 'True':
            resolved = True
        elif resolved == 'false' or resolved == 'False':
            resolved = False
        else:
            resolved = ' '

        if resolved == True or resolved == False:
            reqs = models.MaintenanceRequest.objects.exclude(resolves__isnull=resolved)

        if order_reqs_by in [f.name for f in models.Student._meta.fields]:
            reqs = reqs.order_by(order_reqs_by)
            
        serializer = serializers.MaintenanceRequestSerializer(reqs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def complaints(self, request, pk=None):
        complaints = models.Complaint.objects.filter(student_id=pk)
        order_complaints_by = request.GET.get('order_complaints_by', None)

        if order_complaints_by in [f.name for f in models.Complaint._meta.fields]:
            complaints = complaints.order_by(order_complaints_by)
            
        serializer = serializers.ComplaintSerializer(complaints, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def foodorders(self, request, pk=None):
        orders = models.FoodOrder.objects.filter(student_id=pk)
        fulfilled = request.GET.get('fulfilled', None)
        order_foodorders_by = request.GET.get('order_foodorders_by', None)

        if fulfilled == 'true' or fulfilled == 'True':
            fulfilled = True
        elif fulfilled == 'false' or fulfilled == 'False':
            fulfilled = False
        else:
            fulfilled = ' '

        if fulfilled == True or fulfilled == False:
            orders = models.FoodOrder.objects.exclude(fulfills__isnull=fulfilled)

        if order_foodorders_by in [f.name for f in models.Fulfills._meta.fields]:
            orders = orders.order_by(order_foodorders_by)
            
        serializer = serializers.FoodOrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['get'])
    def packages(self, request, pk=None):
        packages = models.Package.objects.filter(student_id=pk)
        order_packages_by = request.GET.get('order_packages_by', None)

        if order_packages_by in [f.name for f in models.Package._meta.fields]:
            packages = packages.order_by(order_packages_by)
            
        serializer = serializers.PackageSerializer(packages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class StaffViewSet(viewsets.ModelViewSet):
    queryset = models.Staff.objects.all()
    serializer_class = serializers.StaffSerializer
    http_method_names = ['get', 'patch']

class TechnicianViewSet(viewsets.ModelViewSet):
    queryset = models.Technician.objects.all()
    serializer_class = serializers.TechnicianSerializer
    http_method_names = ['get', 'patch']

class AdminViewSet(viewsets.ModelViewSet):
    queryset = models.Admin.objects.all()
    serializer_class = serializers.AdminSerializer
    http_method_names = ['get', 'patch']

class ChefViewSet(viewsets.ModelViewSet):
    queryset = models.Chef.objects.all()
    serializer_class = serializers.ChefSerializer
    http_method_names = ['get', 'patch']

class BuildingViewSet(viewsets.ModelViewSet):
    queryset = models.Building.objects.all()
    serializer_class = serializers.BuildingSerializer

    @action(detail=True, methods=['get', 'post'])
    def rooms(self, request, pk=None):
        building = self.get_object()
        self.serializer_class = serializers.RoomPostSerializer

        if request.method == 'POST':
            data = {
                'building_id': building.building_id,
                'room_no': request.data['room_no'],
                'student_id': '',
            }

            serializer = serializers.RoomSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        else:

            empty = request.GET.get('empty', None)
            
            if empty == 'true' or empty == 'True':
                empty = True
            elif empty == 'false' or empty == 'False':
                empty = False
            else:
                empty = ' '
            
            rooms = models.Room.objects.filter(building_id=pk)

            if empty == True or empty == False:
                rooms = rooms.filter(student_id__isnull=empty)

            serializer = serializers.RoomSerializer(rooms, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

class RoomViewSet(viewsets.ModelViewSet):
    queryset = models.Room.objects.all()
    serializer_class = serializers.RoomSerializer
    http_method_names = ['get', 'patch']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.RoomSerializer
        if self.request.method == 'PATCH':
            return serializers.RoomPatchSerializer

    def get_queryset(self):
        if self.request.method == 'GET':
            queryset = models.Room.objects.all()
            order_by = self.request.GET.get('order_by', None)
            empty = self.request.GET.get('empty', None)

            if empty == 'true' or empty == 'True':
                empty = True
            elif empty == 'false' or empty == 'False':
                empty = False
            else:
                empty = ' '           

            if empty == True or empty == False:
                queryset = queryset.filter(student_id__isnull=empty)
            
            if order_by is not None:
                queryset = queryset.order_by(order_by)
            
            return queryset

        return models.Room.objects.all()

class MaintenanceRequestViewSet(viewsets.ModelViewSet):
    queryset = models.MaintenanceRequest.objects.all()
    serializer_class = serializers.MaintenanceRequestSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.MaintenanceRequestPostSerializer
        if self.request.method == 'GET':
            return serializers.MaintenanceRequestSerializer
        return serializers.MaintenanceRequestSerializer

    def create(self, request):
        student = request.data['student_id']
        print(student)
        try: 
            room = models.Room.objects.get(student_id=student)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        data = {
            'description': request.data['description'], 
            'room_id': room.room_id,
            'student_id': request.data['student_id']
        }

        serializer = serializers.MaintenanceRequestSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class ResolvesViewSet(viewsets.ModelViewSet):
    queryset = models.Resolves.objects.all()
    serializer_class = serializers.ResolvesSerializer

class ComplaintViewSet(viewsets.ModelViewSet):
    queryset = models.Complaint.objects.all()
    serializer_class = serializers.ComplaintSerializer

class FoodOrderViewSet(viewsets.ModelViewSet):
    queryset = models.FoodOrder.objects.all()
    serializer_class = serializers.FoodOrderSerializer

class FulfillsViewSet(viewsets.ModelViewSet):
    queryset = models.Fulfills.objects.all()
    serializer_class = serializers.FulfillsSerializer

class PackageViewSet(viewsets.ModelViewSet):
    queryset = models.Package.objects.all()
    serializer_class = serializers.PackageSerializer

