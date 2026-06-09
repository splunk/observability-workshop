# ITSI Search Examples for Observability Cloud Alerts

These SPL snippets assume Splunk Observability Cloud detector notifications are sent to a Splunk platform index named `o11y_alerts`.

Adjust field names after inspecting your payload. The Splunk Observability Cloud to Splunk platform integration includes `sflo_dimensions`, but automatic field extraction can differ between Splunk platform deployments.

## Normalize Alert Fields

Use this as the base for KPI searches and notable event aggregation:

```spl
index=o11y_alerts sflo_dimensions
| spath
| eval dims=coalesce(sflo_dimensions, 'event.sflo_dimensions')
| spath input=dims
| eval business_application=coalesce(business_application, 'event.business_application', 'business.application', 'sflo_dimensions.business.application', 'event.sflo_dimensions.business.application', "astronomy-shop")
| eval business_transaction=coalesce(business_transaction, 'event.business_transaction', 'business.transaction', 'sflo_dimensions.business.transaction', 'event.sflo_dimensions.business.transaction', "Unmapped")
| eval business_criticality=coalesce(business_criticality, 'event.business_criticality', 'business.criticality', 'sflo_dimensions.business.criticality', 'event.sflo_dimensions.business.criticality', "unknown")
| eval impacted_service=coalesce(impacted_service, 'event.impacted_service', sf_service, 'service.name', 'sflo_dimensions.sf_service', 'sflo_dimensions.service.name', 'event.sflo_dimensions.sf_service')
| eval detector=coalesce(sflo_detector, detector, 'event.sflo_detector')
| eval alert_state=case(match(lower(coalesce(sflo_event_type, eventType, status, "")), "clear|resolved|ok"), "clear", true(), "active")
| fields _time business_application business_transaction business_criticality impacted_service detector alert_state sflo_event_type
```

## KPI: Active O11y Alerts by Transaction

```spl
index=o11y_alerts sflo_dimensions earliest=-30m
| spath
| eval dims=coalesce(sflo_dimensions, 'event.sflo_dimensions')
| spath input=dims
| eval business_transaction=coalesce(business_transaction, 'event.business_transaction', 'business.transaction', 'sflo_dimensions.business.transaction', 'event.sflo_dimensions.business.transaction', "Unmapped")
| eval alert_state=case(match(lower(coalesce(sflo_event_type, eventType, status, "")), "clear|resolved|ok"), "clear", true(), "active")
| stats latest(alert_state) as latest_state by business_transaction sflo_detector
| where latest_state="active"
| stats count as active_alerts by business_transaction
```

## KPI: Latest Impacted Technical Service

```spl
index=o11y_alerts sflo_dimensions earliest=-30m
| spath
| eval dims=coalesce(sflo_dimensions, 'event.sflo_dimensions')
| spath input=dims
| eval business_transaction=coalesce(business_transaction, 'event.business_transaction', 'business.transaction', 'sflo_dimensions.business.transaction', 'event.sflo_dimensions.business.transaction', "Unmapped")
| eval impacted_service=coalesce(impacted_service, 'event.impacted_service', sf_service, 'service.name', 'sflo_dimensions.sf_service', 'sflo_dimensions.service.name', 'event.sflo_dimensions.sf_service')
| stats latest(_time) as last_seen latest(impacted_service) as impacted_service by business_transaction
| convert ctime(last_seen)
```

## KPI: Estimated Revenue at Risk

Replace the inline estimates with your approved business impact model.

```spl
index=o11y_alerts sflo_dimensions earliest=-30m
| spath
| eval dims=coalesce(sflo_dimensions, 'event.sflo_dimensions')
| spath input=dims
| eval business_transaction=coalesce(business_transaction, 'event.business_transaction', 'business.transaction', 'sflo_dimensions.business.transaction', 'event.sflo_dimensions.business.transaction', "Unmapped")
| eval alert_state=case(match(lower(coalesce(sflo_event_type, eventType, status, "")), "clear|resolved|ok"), "clear", true(), "active")
| stats latest(alert_state) as latest_state min(_time) as first_seen by business_transaction sflo_detector
| where latest_state="active"
| eval minutes_active=max(round((now()-first_seen)/60, 1), 1)
| eval revenue_per_minute=case(
    business_transaction="Complete Checkout", 500,
    business_transaction="Manage Cart", 250,
    business_transaction="Confirm Order", 200,
    business_transaction="Browse Catalog", 100,
    true(), 0)
| eval estimated_revenue_at_risk=minutes_active*revenue_per_minute
| stats sum(estimated_revenue_at_risk) as estimated_revenue_at_risk by business_transaction
```

## Episode Aggregation Normalization

Use these fields in an ITSI aggregation policy:

```spl
index=o11y_alerts sflo_dimensions
| spath
| eval dims=coalesce(sflo_dimensions, 'event.sflo_dimensions')
| spath input=dims
| eval business_application=coalesce(business_application, 'event.business_application', 'business.application', 'sflo_dimensions.business.application', "astronomy-shop")
| eval business_transaction=coalesce(business_transaction, 'event.business_transaction', 'business.transaction', 'sflo_dimensions.business.transaction', "Unmapped")
| eval impacted_service=coalesce(impacted_service, 'event.impacted_service', sf_service, 'sflo_dimensions.sf_service', 'sflo_dimensions.service.name')
| eval normalized_title="O11y impact: ".business_transaction." via ".coalesce(impacted_service, "unknown service")
| eval itsi_group_id=business_application."::".business_transaction."::".coalesce(sflo_detector, detector, "unknown_detector")
```
