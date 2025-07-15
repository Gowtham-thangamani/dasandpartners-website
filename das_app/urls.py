from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('about-us', about, name='about'),
    path('our-expertise', our_expertise, name='our_expertise'),
    path('our-work', our_work, name='our_work'),
    path('news', news, name='news'),
    path('blogs', blogs, name='blogs'),
    path('blog/<slug:slug>', blog_details, name='blog_details'),
    path('careers', careers, name='careers'),
    path('contact-us', contact, name='contact'),

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

    path('life-at-dap', life_at_dap, name='life_at_dap'),

    path('login', login, name='login'),

    path('subscribe/', subscribe_newsletter, name='subscribe_newsletter'),
    

]
