# Sequence Diagrams

## 1) User Registration
```mermaid
sequenceDiagram
    autonumber
    actor Client
    participant API as API Controller
    participant Facade as BL Facade
    participant Svc as UserService
    participant Repo as UserRepository
    participant DB as Database

    Client->>API: POST /users {first_name,last_name,email,password}
    API->>API: Validate schema (required fields, email format)
    API->>Facade: register_user(dto)
    Facade->>Svc: validate_and_create(dto)

    Svc->>Repo: checkEmailExists(email)
    Repo->>DB: query
    DB-->>Repo: exists?/not
    Repo-->>Svc: exists?/not

    alt Email already used
        Svc-->>Facade: EmailTakenError
        Facade-->>API: EmailTakenError
        API-->>Client: 409 Conflict {message:"email already used"}
    else New email
        Svc->>Svc: hash = hash(password)
        Svc->>Repo: persistUser(user{first,last,email,hash})
        Repo->>DB: persist
        DB-->>Repo: ok (id, timestamps)
        Repo-->>Svc: User(created)
        Svc-->>Facade: UserDTO
        Facade-->>API: UserDTO
        API-->>Client: 201 Created {id,email,first_name,last_name,created_at}
    end
```
**Explanatory Notes:**  
API call for registers a new user in the system.  
- **Presentation Layer:** Receives the POST request, validates the JSON schema for required fields and email format. Passes the validated data to the Business Logic Layer through the Facade.  
- **Business Logic Layer:** The Facade delegates to `UserService`, which checks if the email already exists. If it does, it returns a 409 Conflict. If not, it hashes the password and prepares a new user entity.  
- **Persistence Layer:** `UserRepository` checks email uniqueness, then persists the user in the database with timestamps.  
The diagram shows both the failure path (duplicate email) and the success path (user creation and returning a 201 Created response).

---

## 2) Place Creation
```mermaid
sequenceDiagram
    autonumber
    actor Client
    participant API as API Controller
    participant Facade as BL Facade
    participant PSvc as PlaceService
    participant ASvc as AmenityService
    participant PRepo as PlaceRepository
    participant ARepo as AmenityRepository
    participant DB as Database

    Client->>API: POST /places {..., amenity_ids?} (Bearer token)
    API->>API: Validate token + schema/constraints
    API->>Facade: create_place(user_id, dto)
    Facade->>PSvc: create_place(user_id, dto)

    opt amenity_ids provided
        PSvc->>ASvc: ensureAmenitiesExist(ids)
        ASvc->>ARepo: findAllByIds(ids)
        ARepo->>DB: query
        DB-->>ARepo: list
        ARepo-->>ASvc: amenities
        alt any missing
            ASvc-->>PSvc: NotFoundError
            PSvc-->>Facade: NotFoundError
            Facade-->>API: NotFoundError
            API-->>Client: 400/404 {message:"invalid amenity id"}
        else all ok
            ASvc-->>PSvc: ok
        end
    end

    PSvc->>PRepo: persistPlace(owner_id, dto)
    PRepo->>DB: persist
    DB-->>PRepo: ok (id, timestamps)
    PRepo-->>PSvc: Place(created)
    PSvc-->>Facade: PlaceDTO
    Facade-->>API: PlaceDTO
    API-->>Client: 201 Created {id, owner_id, ...}
```
**Explanatory Notes:**  
API call for creates a new place owned by the authenticated user.  
- **Presentation Layer:** Validates the bearer token, ensures schema constraints (price, location), and forwards data to the Facade.  
- **Business Logic Layer:** The Facade calls `PlaceService`. If amenity IDs are provided, `AmenityService` verifies their existence. Missing amenities trigger a 400/404 error; otherwise, the place is created.  
- **Persistence Layer:** `PlaceRepository` persists the place. `AmenityRepository` is used to validate amenity IDs.  
The diagram shows optional amenity validation, error handling, and the success path returning a 201 Created.

---

## 3) Review Submission
```mermaid
sequenceDiagram
    autonumber
    actor Client
    participant API as API Controller
    participant Facade as BL Facade
    participant RSvc as ReviewService
    participant PRepo as PlaceRepository
    participant RRepo as ReviewRepository
    participant DB as Database

    Client->>API: POST /places/:id/reviews {rating, comment} (Bearer token)
    API->>API: Validate token + schema (rating 1..5)
    API->>Facade: submit_review(user_id, place_id, dto)
    Facade->>RSvc: submit_review(user_id, place_id, dto)

    RSvc->>PRepo: findPlaceById(place_id)
    PRepo->>DB: query
    DB-->>PRepo: place?/null
    PRepo-->>RSvc: place?/null

    alt place not found
        RSvc-->>Facade: NotFoundError(place)
        Facade-->>API: NotFoundError
        API-->>Client: 404 Not Found
    else place exists
        RSvc->>RRepo: persistReview(user_id, place_id, rating, comment)
        RRepo->>DB: persist
        DB-->>RRepo: ok (id, timestamps)
        RRepo-->>RSvc: Review(created)
        RSvc-->>Facade: ReviewDTO
        Facade-->>API: ReviewDTO
        API-->>Client: 201 Created {id, place_id, user_id, rating, comment}
    end
```
**Explanatory Notes:**  
API call for submits a new review for a place.  
- **Presentation Layer:** Validates authentication token and review schema (rating range). Passes data to the Business Logic Layer via the Facade.  
- **Business Logic Layer:** The Facade calls `ReviewService`, which checks if the place exists. If not, it returns 404; otherwise, it persists the review.  
- **Persistence Layer:** `PlaceRepository` verifies place existence; `ReviewRepository` saves the review.  
The diagram includes both the failure path (place not found) and the success path (review created and returned in the response).

---

## 4) Fetching a List of Places
```mermaid
sequenceDiagram
    autonumber
    actor Client
    participant API as API Controller
    participant Facade as BL Facade
    participant PSvc as PlaceService
    participant PRepo as PlaceRepository
    participant DB as Database

    Client->>API: GET /places?filters...
    API->>API: Parse + validate query params (pagination defaults)
    API->>Facade: list_places(filterSpec, pagination)
    Facade->>PSvc: list_places(filterSpec, pagination)

    PSvc->>PRepo: findAll(filterSpec, pagination)
    PRepo->>DB: query
    DB-->>PRepo: results + total
    PRepo-->>PSvc: Page<Place>
    PSvc-->>Facade: Page<PlaceDTO>
    Facade-->>API: Page<PlaceDTO>
    API-->>Client: 200 OK {items:[...], page, size, total}
```
**Explanatory Notes:**  
API call for retrieves a filtered, paginated list of places.  
- **Presentation Layer:** Parses query parameters, validates them, sets default pagination, and sends request to the Facade.  
- **Business Logic Layer:** The Facade delegates to `PlaceService`, which retrieves the list from the repository and converts entities to DTOs.  
- **Persistence Layer:** `PlaceRepository` queries the database using the filter specification and pagination settings, returning results with total count.  
The diagram shows the complete flow from request parsing to returning the final paginated list with a 200 OK response.

