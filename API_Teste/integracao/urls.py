from django.urls import path
from . import views, views_provisionamento as prov

urlpatterns = [
    path('capacidades/', views.CapacidadesView.as_view()),

    path('provisionar/template/', prov.TemplateProvisionamentoView.as_view()),
    path('provisionar/<slug:codigo>/', prov.DesprovisionarSistemaView.as_view()),
    path('provisionar/', prov.ProvisionarSistemaView.as_view()),

    path('webhooks/<slug:sistema>/<slug:evento>/', views.WebhookReceberView.as_view()),
    path('<slug:sistema>/<slug:operacao>/dry-run/', views.DryRunView.as_view()),
    path('<slug:sistema>/<slug:operacao>/', views.ExecutarOperacaoView.as_view()),

    path('historico/', views.HistoricoIntegracaoView.as_view()),
]