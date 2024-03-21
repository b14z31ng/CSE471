from django.shortcuts import render, redirect, get_object_or_404
from .models import AllProperty, UserProfile
from .forms import *
from django.contrib import messages
from django.db.models import Q
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from urllib.parse import urlencode

def add_property(request):
    if request.session.get('isLoggedIn', False):
        
        if request.method == 'POST':
            form = PropertyTypeForm(request.POST)
            if form.is_valid():
                selected_type = form.cleaned_data['Type']
                if selected_type in ['commercial', 'land', 'residential']:                    
                    return redirect('add_property_data', property_type=selected_type)
                
        else:
            form = PropertyTypeForm()

        return render(request, 'add_property.html', {'form':form})

    else:
        return redirect(reverse('signin') + '?next=' + request.path)
    
@login_required
def add_property_data(request, property_type):
    if property_type == 'commercial':
        form_class = CommercialPropertyForm
    elif property_type == 'land':
        form_class = LandPropertyForm
    elif property_type == 'residential':
        form_class = ResidentialPropertyForm
    else:
        return redirect('add_property')

    if request.method == 'POST':
        user_profile = UserProfile.objects.get(user=request.user)
        form = form_class(request.POST, request.FILES)
        
        if form.is_valid():
            property_instance = form.save(commit=False)
            property_instance.user = user_profile
            property_instance.Property_type = property_type
            property_instance.save()

            messages.success(request, "Property added Successfully")
            return redirect('property_list')

        else:
            messages.error(request, "Something went wrong!")  
    else:
        form = form_class()
    return render(request, 'add_property_data.html', {'form': form, 'property_type':property_type})

@login_required
def update_property(request, property_id):
    property_instance = AllProperty.objects.get(pk=property_id)
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES, instance=property_instance)
        if form.is_valid():
            form.save()
            messages.success(request, "Property updated Successfully")
            return redirect('property_list')  
        
    else:
        form = PropertyForm(instance=property_instance)
        
    return render(request, 'update_property.html', {'form': form})

def property_detail(request, pk):
    property_instance = AllProperty.objects.get(pk = pk)
    
    if hasattr(property_instance, 'residentialproperty'):
        specific_property_instance = property_instance.residentialproperty
    elif hasattr(property_instance, 'commercialproperty'):
        specific_property_instance = property_instance.commercialproperty
    elif hasattr(property_instance, 'landproperty'):
        specific_property_instance = property_instance.landproperty
    else:
        # Handle the case where the property instance does not belong to any specific type
        specific_property_instance = None


    property_fields = {}
    
    if(specific_property_instance):
        property_fields = vars(specific_property_instance)
        property_fields['Property_Pictures'] = property_instance.Property_Pictures


    return render(request, "property_detail.html", {'property_fields':property_fields})



def property_list(request):
    properties = AllProperty.objects.all()

    # Create an instance of the form
    filter_form = PropertyFilterForm(request.GET or None)
    saved_searches = SavedSearch.objects.filter(user=request.user)[:5]

    # Check if form is submitted and valid
    if filter_form.is_valid():
        # Get cleaned data from the form
        cleaned_data = filter_form.cleaned_data
        property_type = cleaned_data.get('property_type')
        property_on = cleaned_data.get('property_on')
        area = cleaned_data.get('area')

        # Filter properties based on form data
        properties = properties.filter(Property_type=property_type) if property_type else properties
        properties = properties.filter(Property_on=property_on) if property_on else properties
        properties = properties.filter(Area=area) if area else properties

        # Additional filters based on property type
        if property_type == 'residential':
            bedrooms = cleaned_data.get('bedrooms')
            bathrooms = cleaned_data.get('bathrooms')

            properties = properties.filter(residentialproperty__Bedrooms=bedrooms) if bedrooms else properties
            properties = properties.filter(residentialproperty__Bathrooms=bathrooms) if bathrooms else properties

        elif property_type == 'commercial':
            business_type = cleaned_data.get('business_type')
            has_conference = cleaned_data.get('has_conference')
            has_security = cleaned_data.get('has_security')

            properties = properties.filter(commercialproperty__Business_type=business_type) if business_type else properties
            properties = properties.filter(commercialproperty__Has_conference_room=True) if has_conference else properties
            properties = properties.filter(commercialproperty__Has_security_system=True) if has_security else properties

        elif property_type == 'land':
            land_type = cleaned_data.get('land_type')

            properties = properties.filter(landproperty__Land_type=land_type) if land_type else properties


        ordering_choice = cleaned_data.get('ordering_choices')
        if ordering_choice == 'price_asc':
            properties = properties.order_by('Price')
        elif ordering_choice == 'price_desc':
            properties = properties.order_by('-Price')

    saved_search_name = request.GET.get('saved_search_name')
    if saved_search_name:
        if request.user.is_authenticated:  
            existing_search = SavedSearch.objects.filter(user=request.user, name=saved_search_name).first()
            if not existing_search:
                SavedSearch.objects.create(user=request.user, name = saved_search_name, criteria = request.GET.dict())

        else:
            return redirect(reverse('signin') + '?next=' + request.path)

    context = {
        'filtered_properties': properties,
        'filter_form': filter_form,
        'saved_searches':saved_searches,
    }
    return render(request, 'property_list.html', context)



def property_type(request):
    return render(request, "property_type.html")


def calculate(request):
    if request.method == 'POST':
        form = PropertyCalculatorForm(request.POST)
        if form.is_valid():
            per_sqft_price = form.cleaned_data['per_sqft_price']
            total_sqft = form.cleaned_data['total_sqft']
            parking_sqft = form.cleaned_data['parking_sqft']
            parking_price_per_sqft = form.cleaned_data['parking_price_per_sqft']
            
            total_amount = (per_sqft_price * total_sqft) + (parking_sqft * parking_price_per_sqft)
            
            return render(request, 'Calculate.html', {'form': form, 'total_amount': total_amount})
    else:
        form = PropertyCalculatorForm()

    return render(request, 'Calculate.html', {'form': form})


def saved_searches(request):
    if request.user.is_authenticated:
        saved_searches = SavedSearch.objects.filter(user=request.user)
        return render(request, 'saved_searches.html', {'saved_searches': saved_searches})
    
    else:
        return render(request, "signin.html")
    
@login_required
def delete_saved_search(request, saved_search_id):
    saved_search = get_object_or_404(SavedSearch, id=saved_search_id)
    if saved_search.user == request.user:
        saved_search.delete()
    return redirect('saved_searches')
    

def apply_saved_search(request, saved_search_id):
    saved_search = get_object_or_404(SavedSearch, id=saved_search_id)
    criteria_str = urlencode(saved_search.criteria)
    # Redirect to property list page with saved search criteria in the query string
    return redirect(reverse('property_list') + '?' + criteria_str)