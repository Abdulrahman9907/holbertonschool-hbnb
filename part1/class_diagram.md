# HBnB Evolution - Business Logic Layer Class Diagram

```mermaid
classDiagram
classDiagram
direction LR

%% ---------- Core abstraction (audit + id everywhere) ----------
class BaseEntity {
  <<abstract>>
  +id: UUIDv4
  +created_at: DateTime
  +updated_at: DateTime
}

%% ---------- User ----------
class User {
  +first_name: String
  +last_name: String
  +email: String  <<unique>>
  +password: String  <<hashed>>
  +is_admin: Boolean
  +register(): void
  +update_profile(first_name: String, last_name: String, email: String, password: String): void
  +delete(): void
}

%% ---------- Place ----------
class Place {
  +title: String
  +description: String
  +price: Decimal  <<>= 0>>
  +latitude: Float  <<-90..90>>
  +longitude: Float <<-180..180>>
  +create(): void
  +update(title: String, description: String, price: Decimal, latitude: Float, longitude: Float): void
  +delete(): void
  +add_amenity(a: Amenity): void
  +remove_amenity(a: Amenity): void
  +list_amenities(): List~Amenity~
  +average_rating(): Float
}

%% ---------- Review ----------
class Review {
  +rating: Int <<1..5>>
  +comment: String
  +create(): void
  +update(rating: Int, comment: String): void
  +delete(): void
}

%% ---------- Amenity ----------
class Amenity {
  +name: String
  +description: String
  +create(): void
  +update(name: String, description: String): void
  +delete(): void
}

%% ---------- Inheritance (DRY: id + audit fields) ----------
BaseEntity <|-- User
BaseEntity <|-- Place
BaseEntity <|-- Review
BaseEntity <|-- Amenity

%% ---------- Relationships & multiplicities ----------
%% User owns Places
User "1" o-- "*" Place : owns

%% User writes Reviews
User "1" --> "*" Review : writes

%% Place has Reviews (composition: delete place => delete its reviews)
Place "1" *-- "*" Review : has

%% Place offers Amenities (many-to-many)
Place "*" -- "*" Amenity : offers

