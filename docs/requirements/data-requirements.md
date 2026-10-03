# Data Requirements

## Purpose

This document defines the initial data entities, required attributes, business keys, relationships, and quality expectations for OpsIntel BI.

The objective is to establish a clear data contract before synthetic data generation begins.

# Core Data Entities

The initial solution requires these major entities:

1. Customer
2. Carrier
3. Region
4. Location
5. Route
6. Asset
7. Shipment
8. Transportation Cost
9. Asset Movement
10. Transportation Budget
11. Operational Exception
12. Date

# Customer

## Purpose

Represents organizations receiving shipments or participating in operational activity.

## Required Attributes

- Customer ID
- Customer Name
- Customer Status
- Customer Segment
- Region
- Created Date
- Inactive Date

## Business Key

```text
Customer ID
```

## Initial Status Values

```text
ACTIVE
INACTIVE
```

## Data Rules

- Customer ID must be unique.
- Customer Name must not be null.
- Historical customers must remain available after becoming inactive.
- Inactive Date should only be populated when Customer Status is `INACTIVE`.

---

# Carrier

## Purpose

Represents transportation providers responsible for shipments.

## Required Attributes

- Carrier ID
- Carrier Name
- Carrier Status
- Transportation Mode
- Primary Region
- Created Date

## Business Key

```text
Carrier ID
```

## Initial Status Values

```text
ACTIVE
INACTIVE
```

## Candidate Transportation Modes

```text
TRUCK
RAIL
AIR
OCEAN
INTERMODAL
```

## Data Rules

- Carrier ID must be unique.
- Carrier Name must not be null.
- Historical activity must remain available for inactive carriers.

---

# Region

## Purpose

Represents major geographic operating areas.

## Required Attributes

- Region ID
- Region Name

## Business Key

```text
Region ID
```

## Initial Regions

```text
North America
Europe
Latin America
```

## Data Rules

- Region ID must be unique.
- Region Name must be unique.
- Every operational location must belong to one region.

---

# Location

## Purpose

Represents operational sites used as shipment origins, destinations, and asset movement locations.

## Required Attributes

- Location ID
- Location Name
- Location Type
- City
- State / Province
- Country
- Region ID
- Latitude
- Longitude
- Active Flag

## Business Key

```text
Location ID
```

## Candidate Location Types

```text
PLANT
WAREHOUSE
SERVICE_CENTER
CUSTOMER_SITE
PORT
```

## Data Rules

- Location ID must be unique.
- Every location must belong to one valid region.
- Latitude and longitude must be valid geographic coordinates when populated.
- Historical locations should not be deleted if they become inactive.

---

# Route

## Purpose

Represents a recurring origin-to-destination transportation lane.

## Required Attributes

- Route ID
- Origin Location ID
- Destination Location ID
- Distance
- Distance Unit
- Expected Transit Days
- Transportation Mode
- Active Flag

## Business Key

```text
Route ID
```

## Conceptual Natural Key

```text
Origin Location ID
+
Destination Location ID
+
Transportation Mode
```

## Data Rules

- Route ID must be unique.
- Origin and destination must reference valid locations.
- Distance must be greater than zero.
- Expected Transit Days must be greater than zero.
- Duplicate active routes with the same natural key should not exist.

---

# Asset

## Purpose

Represents reusable logistics assets moving through the network.

## Required Attributes

- Asset ID
- Asset Type
- Asset Status
- Home Location ID
- Current Location ID
- Created Date
- Retirement Date

## Business Key

```text
Asset ID
```

## Initial Status Values

```text
AVAILABLE
IN_USE
IN_TRANSIT
MAINTENANCE
LOST
RETIRED
```

## Data Rules

- Asset ID must be unique.
- Asset Status must use an approved value.
- Home Location must reference a valid location.
- Retirement Date should only exist for retired assets.

---

# Shipment

## Purpose

Represents one shipment from an origin location to a destination location.

## Required Attributes

- Shipment ID
- Customer ID
- Carrier ID
- Route ID
- Origin Location ID
- Destination Location ID
- Shipment Date
- Expected Delivery Date
- Actual Delivery Date
- Shipment Status
- Shipment Quantity
- Transportation Mode
- Created Timestamp

## Business Key

```text
Shipment ID
```

## Initial Status Values

```text
PLANNED
IN_TRANSIT
DELIVERED
CANCELLED
```

## Data Rules

- Shipment ID must be unique.
- Customer ID must reference a valid customer.
- Carrier ID must reference a valid carrier when applicable.
- Route ID must reference a valid route.
- Origin and destination must match the assigned route.
- Shipment Quantity must be greater than zero.
- Delivered shipments should contain an Actual Delivery Date.
- Cancelled shipments should not contribute to delivery-performance metrics.
- Actual Delivery Date must not precede Shipment Date for valid delivered records.

---

# Transportation Cost

## Purpose

Represents cost transactions associated with shipment activity.

## Required Attributes

- Transportation Cost ID
- Shipment ID
- Cost Date
- Cost Type
- Cost Amount
- Currency
- Transaction Type
- Created Timestamp

## Business Key

```text
Transportation Cost ID
```

## Candidate Cost Types

```text
BASE_FREIGHT
FUEL_SURCHARGE
ACCESSORIAL
TOLL
HANDLING
CORRECTION
```

## Candidate Transaction Types

```text
CHARGE
CREDIT
REVERSAL
```

## Data Rules

- Transportation Cost ID must be unique.
- Shipment ID must reference a valid shipment.
- A shipment may have multiple transportation cost records.
- Negative amounts are allowed for valid credits or reversals.
- Currency must be present even though multi-currency conversion is initially out of scope.

---

# Asset Movement

## Purpose

Represents the movement or status transition of a reusable asset.

## Required Attributes

- Asset Movement ID
- Asset ID
- Movement Timestamp
- Origin Location ID
- Destination Location ID
- Movement Type
- Previous Status
- New Status
- Related Shipment ID

## Business Key

```text
Asset Movement ID
```

## Candidate Movement Types

```text
SHIPMENT
RETURN
REPOSITION
MAINTENANCE_TRANSFER
STATUS_CHANGE
```

## Data Rules

- Asset Movement ID must be unique.
- Asset ID must reference a valid asset.
- Related Shipment ID may be null when the movement is not shipment-related.
- Status transitions should follow documented business logic.
- Origin or destination may be null only when justified by the movement type.

---

# Transportation Budget

## Purpose

Represents planned transportation spending.

## Required Attributes

- Budget ID
- Budget Month
- Region ID
- Budget Amount
- Currency
- Created Timestamp

## Business Key

```text
Budget ID
```

## Analytical Grain

```text
One row per Month + Region
```

## Data Rules

- Region ID must reference a valid region.
- Budget Amount must be greater than or equal to zero.
- Duplicate Month + Region budget records should not exist.

---

# Operational Exception

## Purpose

Represents an operational event requiring attention.

## Required Attributes

- Exception ID
- Exception Type
- Exception Date
- Severity
- Shipment ID
- Asset ID
- Customer ID
- Carrier ID
- Route ID
- Location ID
- Description
- Resolved Flag
- Resolution Date

## Business Key

```text
Exception ID
```

## Initial Exception Types

```text
LATE_DELIVERY
CANCELLED_SHIPMENT
MISSING_ASSET
DAMAGED_ASSET
COST_ANOMALY
ROUTE_EXCEPTION
```

## Initial Severity Values

```text
LOW
MEDIUM
HIGH
CRITICAL
```

## Data Rules

- Exception ID must be unique.
- Exception Type must use an approved value.
- Severity must use an approved value.
- At least one related business entity should normally be present.
- Resolution Date should only exist when the exception is resolved.

---

# Date

## Purpose

Provides the governed calendar dimension used for time intelligence.

## Required Attributes

- Date
- Date Key
- Day
- Day Name
- Day of Week
- Week Number
- Month Number
- Month Name
- Quarter
- Year
- Year-Month
- Is Weekend

## Business Key

```text
Date
```

## Data Rules

- One row must exist for every calendar date in the supported reporting range.
- Dates must be continuous with no gaps.
- Date Key should be unique.
- Calendar-year reporting will be used initially.

# Initial Dataset Scale

The synthetic dataset should be large enough to demonstrate realistic analytical behavior without becoming unnecessarily difficult to manage locally.

Initial targets:

```text
Regions                     3
Locations                  60-100
Customers                 250-400
Carriers                   15-30
Routes                    200-500
Assets                  3,000-6,000
Shipments              75,000-150,000
Transportation Costs  100,000-300,000
Asset Movements        200,000-500,000
Budgets                    ~108
Operational Exceptions  5,000-20,000
Dates                     ~1,100
```

The exact volume may be adjusted based on local performance and learning needs.

# Historical Time Range

The initial dataset should contain approximately three years of historical data.

The date range should support:

- monthly trends
- Year-to-Date analysis
- previous-year comparisons
- seasonal behavior
- budget variance analysis

# Data Quality Scenarios

The generated dataset should deliberately contain controlled data-quality issues.

Candidate scenarios include:

- missing carrier reference
- duplicate shipment record
- missing expected delivery date
- invalid actual delivery date
- zero or negative shipment quantity
- unusually high transportation cost
- missing customer reference
- orphaned operational exception
- invalid asset status transition
- duplicate budget record

These records should be rare enough that the dataset remains analytically usable.

# Referential Integrity Requirements

The generated dataset should preserve expected relationships except where a controlled data-quality test explicitly violates them.

Examples:

```text
Shipment.CustomerID -> Customer.CustomerID
Shipment.CarrierID -> Carrier.CarrierID
Shipment.RouteID -> Route.RouteID
Route.OriginLocationID -> Location.LocationID
Route.DestinationLocationID -> Location.LocationID
TransportationCost.ShipmentID -> Shipment.ShipmentID
AssetMovement.AssetID -> Asset.AssetID
Budget.RegionID -> Region.RegionID
```

# Reproducibility Requirement

Synthetic data generation should be deterministic when supplied the same random seed.

This allows:

- repeatable tests
- stable debugging
- reproducible screenshots
- consistent SQL validation
- reliable portfolio demonstrations

# Data Generation Principle

The synthetic dataset should not be purely random.

The data should contain meaningful patterns such as:

- seasonal shipment volume
- regional cost differences
- carrier performance differences
- route distance effects
- service-level variation
- customer concentration
- asset-utilization variation
- controlled anomalies

These patterns should make it possible to discover realistic analytical insights in later phases.