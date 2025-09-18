#!/bin/bash

# End-to-End Testing Script for HBnB API
# This script tests all the implemented functionality

echo "=========================================="
echo "HBnB API End-to-End Testing"
echo "=========================================="

BASE_URL="http://127.0.0.1:5000/api/v1"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counter
TESTS=0
PASSED=0

test_endpoint() {
    TESTS=$((TESTS + 1))
    local description="$1"
    local method="$2"
    local endpoint="$3"
    local data="$4"
    local auth_header="$5"
    local expected_status="$6"

    echo -e "\n${YELLOW}Test $TESTS: $description${NC}"

    if [ "$method" = "GET" ]; then
        if [ -n "$auth_header" ]; then
            response=$(curl -s -w "\n%{http_code}" -X GET "$BASE_URL$endpoint" -H "$auth_header")
        else
            response=$(curl -s -w "\n%{http_code}" -X GET "$BASE_URL$endpoint")
        fi
    elif [ "$method" = "POST" ]; then
        if [ -n "$auth_header" ]; then
            response=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL$endpoint" -H "Content-Type: application/json" -H "$auth_header" -d "$data")
        else
            response=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL$endpoint" -H "Content-Type: application/json" -d "$data")
        fi
    elif [ "$method" = "PUT" ]; then
        response=$(curl -s -w "\n%{http_code}" -X PUT "$BASE_URL$endpoint" -H "Content-Type: application/json" -H "$auth_header" -d "$data")
    elif [ "$method" = "DELETE" ]; then
        response=$(curl -s -w "\n%{http_code}" -X DELETE "$BASE_URL$endpoint" -H "$auth_header")
    fi

    # Extract status code (last line)
    status_code=$(echo "$response" | tail -n1)
    # Extract response body (all but last line)
    response_body=$(echo "$response" | head -n -1)

    echo "Status: $status_code"
    echo "Response: $response_body"

    if [ "$status_code" = "$expected_status" ]; then
        echo -e "${GREEN}✓ PASSED${NC}"
        PASSED=$((PASSED + 1))
    else
        echo -e "${RED}✗ FAILED (Expected: $expected_status, Got: $status_code)${NC}"
    fi
}

echo -e "\n${YELLOW}=== 1. Testing User Registration (Admin Only) ===${NC}"

# Test user registration without token (should fail)
test_endpoint "User registration without auth" "POST" "/users/" '{
    "first_name": "Test",
    "last_name": "User",
    "email": "test@example.com",
    "password": "testpass123"
}' "" "422"

echo -e "\n${YELLOW}=== 2. Testing Authentication ===${NC}"

# Test admin login
test_endpoint "Admin login" "POST" "/auth/login" '{
    "email": "admin@hbnb.io",
    "password": "admin1234"
}' "" "200"

# Extract token from login response (assuming it worked)
login_response=$(curl -s -X POST "$BASE_URL/auth/login" -H "Content-Type: application/json" -d '{
    "email": "admin@hbnb.io",
    "password": "admin1234"
}')

if echo "$login_response" | grep -q "access_token"; then
    ADMIN_TOKEN=$(echo "$login_response" | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)
    echo "Admin token obtained: ${ADMIN_TOKEN:0:20}..."
else
    echo -e "${RED}Failed to get admin token. Testing will be limited.${NC}"
    ADMIN_TOKEN=""
fi

echo -e "\n${YELLOW}=== 3. Testing Public Endpoints ===${NC}"

# Test getting all places (public)
test_endpoint "Get all places (public)" "GET" "/places/" "" "" "200"

# Test getting all users (public)
test_endpoint "Get all users (public)" "GET" "/users/" "" "" "200"

# Test getting all amenities (public)
test_endpoint "Get all amenities (public)" "GET" "/amenities/" "" "" "200"

if [ -n "$ADMIN_TOKEN" ]; then
    echo -e "\n${YELLOW}=== 4. Testing Admin Functions ===${NC}"

    # Test creating a regular user (admin only)
    test_endpoint "Create regular user (admin)" "POST" "/users/" '{
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "password": "password123"
    }' "Authorization: Bearer $ADMIN_TOKEN" "201"

    # Test creating an amenity (admin only)
    test_endpoint "Create amenity (admin)" "POST" "/amenities/" '{
        "name": "Test Amenity"
    }' "Authorization: Bearer $ADMIN_TOKEN" "201"

    echo -e "\n${YELLOW}=== 5. Testing Regular User Functions ===${NC}"

    # Login as regular user
    user_login_response=$(curl -s -X POST "$BASE_URL/auth/login" -H "Content-Type: application/json" -d '{
        "email": "john.doe@example.com",
        "password": "password123"
    }')

    if echo "$user_login_response" | grep -q "access_token"; then
        USER_TOKEN=$(echo "$user_login_response" | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)
        echo "User token obtained: ${USER_TOKEN:0:20}..."

        # Test creating a place
        test_endpoint "Create place (user)" "POST" "/places/" '{
            "title": "Test Place",
            "description": "A nice test place",
            "price": 100.50,
            "latitude": 37.7749,
            "longitude": -122.4194
        }' "Authorization: Bearer $USER_TOKEN" "201"

        # Get place ID from response (for further testing)
        place_response=$(curl -s -X POST "$BASE_URL/places/" -H "Content-Type: application/json" -H "Authorization: Bearer $USER_TOKEN" -d '{
            "title": "Review Test Place",
            "description": "A place for review testing",
            "price": 200.00,
            "latitude": 40.7128,
            "longitude": -74.0060
        }')

        if echo "$place_response" | grep -q '"id"'; then
            PLACE_ID=$(echo "$place_response" | grep -o '"id":"[^"]*"' | cut -d'"' -f4)
            echo "Place created with ID: $PLACE_ID"

            echo -e "\n${YELLOW}=== 6. Testing Review Functions ===${NC}"

            # Test that admin can create review for user's place
            test_endpoint "Create review (admin)" "POST" "/reviews/" '{
                "text": "Great place!",
                "rating": 5,
                "place_id": "'$PLACE_ID'"
            }' "Authorization: Bearer $ADMIN_TOKEN" "201"

            # Test that user cannot review their own place
            test_endpoint "User review own place (should fail)" "POST" "/reviews/" '{
                "text": "My own place",
                "rating": 5,
                "place_id": "'$PLACE_ID'"
            }' "Authorization: Bearer $USER_TOKEN" "400"
        fi

        echo -e "\n${YELLOW}=== 7. Testing Authorization ===${NC}"

        # Test that regular user cannot create other users
        test_endpoint "Regular user create user (should fail)" "POST" "/users/" '{
            "first_name": "Unauthorized",
            "last_name": "User",
            "email": "unauthorized@example.com",
            "password": "password123"
        }' "Authorization: Bearer $USER_TOKEN" "403"

        # Test that regular user cannot create amenities
        test_endpoint "Regular user create amenity (should fail)" "POST" "/amenities/" '{
            "name": "Unauthorized Amenity"
        }' "Authorization: Bearer $USER_TOKEN" "403"

    else
        echo -e "${RED}Failed to login as regular user${NC}"
    fi
fi

echo -e "\n${YELLOW}=== 8. Testing Invalid Scenarios ===${NC}"

# Test login with invalid credentials
test_endpoint "Invalid login" "POST" "/auth/login" '{
    "email": "invalid@example.com",
    "password": "wrongpassword"
}' "" "401"

# Test accessing protected endpoint without token
test_endpoint "Protected endpoint without token" "POST" "/places/" '{
    "title": "Unauthorized Place"
}' "" "422"

echo -e "\n=========================================="
echo -e "${GREEN}TESTING COMPLETE${NC}"
echo -e "Tests run: $TESTS"
echo -e "Tests passed: $PASSED"
echo -e "Tests failed: $((TESTS - PASSED))"

if [ $PASSED -eq $TESTS ]; then
    echo -e "${GREEN}All tests passed! ✓${NC}"
    exit 0
else
    echo -e "${RED}Some tests failed! ✗${NC}"
    exit 1
fi