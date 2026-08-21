from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('about-us', about, name='about'),
    path('our-expertise', our_expertise, name='our_expertise'),
    path('our-work', our_work, name='our_work'),
    path('news', news, name='news'),
    path('news/<slug:slug>', news_details, name='news_details'),
    path('blogs', blogs, name='blogs'),
    path('blog/<slug:slug>', blog_details, name='blog_details'),
    path('careers', careers, name='careers'),
    path('contact-us', contact, name='contact'),
    path('our-people', our_people, name='our_people'),
    path('gallery', gallery, name='gallery'),
    path('architectural-engineering', architectural_engineering, name='architectural_engineering'),
    path('architect-of-record', architect_of_record, name='architect_of_record'),
    path('oil-and-gas-engineering', oil_and_gas_engineering, name='oil_and_gas_engineering'),
    path('structural-engineering', structural_engineering, name='structural_engineering'),
    path('infrastructure', infrastructure, name='infrastructure'),
    path('construction-engineering', construction_engineering, name='construction_engineering'),
    path('mep-engineering', mep_engineering, name='mep_engineering'),
    path('project_management', project_management, name='project_management'),
    path('villa_design', villa_design, name='villa_design'),
    path('villa-design-abu-dhabi', villa_design_abu_dhabi, name='villa_design_abu_dhabi'),
    path('interior_design', interior_design, name='interior_design'),
    path('building-information-modeling', building_information_modeling, name='building_information_modeling'),
    path('lead-consultant', lead_consultant, name='lead_consultant'),
    path('contract-cost-consultancy', contract_cost_consultancy, name='contract_cost_consultancy'),
    path('facilities-management-consultancy', facilities_management_consultancy, name='facilities_management_consultancy'),
    path('renewable-energy-consultants', renewable_energy_consultants, name='renewable_energy_consultants'),
    path('mall-management-consultants', mall_management_consultants, name='mall_management_consultants'),
    path('leed-consultants', leed_consultants, name='leed_consultants'),
    path('electrical-engineering-consultancy', electrical_engineering_consultancy, name='electrical_engineering_consultancy'),

    path('life', life_at_dap, name='life_at_dap'),

    path('login', login, name='login'),

    path('subscribe/', subscribe_newsletter, name='subscribe_newsletter'),

    # New Service URLs
    path('csa-services', csa_services, name='csa_services'),
    path('mep-services', mep_services, name='mep_services'),
    path('eit-services', eit_services, name='eit_services'),
    path('hsse-services', hsse_services, name='hsse_services'),
    path('bim-services', bim_services, name='bim_services'),
    path('contract-administration', contract_administration, name='contract_administration'),

    # Unified expertise URL pattern
    path('expertise/<str:expertise_key>', unified_expertise, name='unified_expertise'),

    # New Expertise URLs
    path('highways-bridges', lambda request: unified_expertise(request, 'highways_bridges'), name='highways_bridges'),
    path('transport-planning', lambda request: unified_expertise(request, 'transport_planning'), name='transport_planning'),
    path('landscaping-public-realm', lambda request: unified_expertise(request, 'landscaping_public_realm'), name='landscaping_public_realm'),
    path('urban-master-planning', lambda request: unified_expertise(request, 'urban_master_planning'), name='urban_master_planning'),
    path('environmental', lambda request: unified_expertise(request, 'environmental'), name='environmental'),
    path('industrial-design', lambda request: unified_expertise(request, 'industrial_design'), name='industrial_design'),
    path('infrastructure-transport', lambda request: unified_expertise(request, 'infrastructure_transport'), name='infrastructure_transport'),
    path('landscape', lambda request: unified_expertise(request, 'landscape'), name='landscape'),
    path('land-surveying', lambda request: unified_expertise(request, 'land_surveying'), name='land_surveying'),
    path('urban-master-planning-2', lambda request: unified_expertise(request, 'urban_master_planning_2'), name='urban_master_planning_2'),
    path('process-engineering', lambda request: unified_expertise(request, 'process_engineering'), name='process_engineering'),

    # Authentication URLs
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    
    # Content Management Portal URLs
    path('content-dashboard/', content_dashboard, name='content_dashboard'),
    path('add-news/', add_news, name='add_news'),
    path('add-blog/', add_blog, name='add_blog'),
    path('news-list/', news_list, name='news_list'),
    path('blog-list/', blog_list, name='blog_list'),
    path('edit-news/<int:news_id>/', edit_news, name='edit_news'),
    path('edit-blog/<int:blog_id>/', edit_blog, name='edit_blog'),
    path('delete-news/<int:news_id>/', delete_news, name='delete_news'),
    path('delete-blog/<int:blog_id>/', delete_blog, name='delete_blog'),

]
