# Explanatory Notes – HBnB Evolution Business Logic Layer

## **Overview**
The Business Logic Layer (BLL) for HBnB Evolution contains the core entities that model the domain rules of the application: **User**, **Place**, **Review**, and **Amenity**.  
All entities inherit from an abstract **BaseEntity** class to ensure a consistent structure with unique identifiers and audit timestamps.

The notes below describe:
- **Attributes** — essential data each entity holds.
- **Methods** — business operations relevant to that entity.
- **Relationships** — connections between entities with multiplicities and ownership semantics.
- **Business rules** — constraints and lifecycle behaviors.

---

## **Entities**

### **BaseEntity** *(abstract)*
- **Role:** Parent class for all entities to enforce common fields: `id`, `created_at`, `updated_at`.
- **Why:** Avoids duplication (DRY) and ensures every entity supports unique identification and auditing.
- **Attributes:**
  - `id: UUIDv4` — globally unique identifier.
  - `created_at: DateTime` — creation timestamp.
  - `updated_at: DateTime` — last modification timestamp.
- **Methods:** None directly; extended by subclasses.

---

### **User**
- **Role:** Represents a registered account (either regular user or administrator).
- **Key Attributes:**
  - `first_name`, `last_name`: Personal details.
  - `email` *(unique)*: Login identifier.
  - `password` *(hashed)*: Authentication credential (secure storage in implementation).
  - `is_admin`: Boolean flag for elevated privileges.
- **Methods:**
  - `register()` — Creates a new account.
  - `update_profile(...)` — Changes personal info and/or password.
  - `delete()` — Removes account (with rules for owned places/reviews).
- **Relationships:**
  - `1 → *` **Place** (owns).
  - `1 → *` **Review** (writes).
- **Business Rules:**
  - `email` must be unique and valid.
  - Passwords stored securely.
  - Ownership transfer or cascade rules apply when deleting.

---

### **Place**
- **Role:** Represents a property listing created by a user.
- **Key Attributes:**
  - `title`, `description`: Listing information.
  - `price`: Non-negative decimal value.
  - `latitude`, `longitude`: Geolocation within valid ranges.
- **Methods:**
  - `create()` — Adds a new listing.
  - `update(...)` — Edits listing details.
  - `delete()` — Removes listing (also deletes related reviews).
  - `add_amenity(a: Amenity)` — Links an amenity to the place (idempotent).
  - `remove_amenity(a: Amenity)` — Unlinks an amenity.
  - `list_amenities()` — Returns all amenities associated with this place.
  - `average_rating()` — Calculates the average review score.
- **Relationships:**
  - `* → 1` **User** (owner).
  - `1 → *` **Review** (composition — reviews deleted with place).
  - `* ↔ *` **Amenity** (many-to-many — offers).
- **Business Rules:**
  - Price ≥ 0.
  - Valid latitude (−90..90) and longitude (−180..180).
  - Amenity list must not contain duplicates.

---

### **Review**
- **Role:** User feedback on a place.
- **Key Attributes:**
  - `rating`: Integer (1..5).
  - `comment`: Review text.
- **Methods:**
  - `create()` — Adds a new review.
  - `update(...)` — Changes rating/comment.
  - `delete()` — Removes review.
- **Relationships:**
  - `* → 1` **User** (author).
  - `* → 1` **Place** (target — composition under Place).
- **Business Rules:**
  - One review per user per place (optional but common).
  - Rating must be within allowed range.
  - Review must belong to an existing Place and User.

---

### **Amenity**
- **Role:** A feature or service that can be linked to a place (e.g., Wi-Fi, pool).
- **Key Attributes:**
  - `name`: Short description (ideally unique).
  - `description`: Longer explanation.
- **Methods:**
  - `create()` — Adds a new amenity type.
  - `update(...)` — Changes name/description.
  - `delete()` — Removes amenity type (removes links but not places).
- **Relationships:**
  - `* ↔ *` **Place** (many-to-many).
- **Business Rules:**
  - Avoid duplicate amenity names.
  - Deletion removes only associations, not linked places.

---

## **Relationships & Multiplicities**
1. **BaseEntity <|-- [User, Place, Review, Amenity]** — generalization for ID/audit.
2. **User "1" o-- "*" Place** — aggregation: user owns many places; places can be reassigned.
3. **User "1" --> "*" Review** — association: user writes many reviews; each review has one author.
4. **Place "1" *-- "*" Review** — composition: place owns reviews; deleting place deletes reviews.
5. **Place "*" -- "*" Amenity** — many-to-many association: places offer amenities; amenities are reusable.

---

## **Design Rationale**
- **BaseEntity** ensures consistent IDs and timestamps.
- Composition used where lifecycle is tightly bound (`Place`–`Review`).
- Aggregation used where reassignments are possible (`User`–`Place`).
- Many-to-many left as a plain association to allow shared amenities.
- Methods are limited to **business actions**, leaving persistence logic to other layers.

