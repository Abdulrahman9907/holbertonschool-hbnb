const API_BASE_URL = 'http://127.0.0.1:5000/api/v1';

// Utility function to get cookie value by name
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

// Function to set a cookie
function setCookie(name, value, days = 7) {
    const expires = new Date();
    expires.setTime(expires.getTime() + days * 24 * 60 * 60 * 1000);
    document.cookie = `${name}=${value};expires=${expires.toUTCString()};path=/`;
}

// Login functionality
document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');

    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            
            // Get email and password from form
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            try {
                const response = await fetch(`${API_BASE_URL}/auth/login`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ email, password })
                });

                if (response.ok) {
                    const data = await response.json();
                    // Store JWT token in cookie
                    setCookie('token', data.access_token);
                    // Redirect to main page
                    window.location.href = 'index.html';
                } else {
                    const errorData = await response.json();
                    alert('Login failed: ' + (errorData.message || response.statusText));
                }
            } catch (error) {
                console.error('Error during login:', error);
                alert('An error occurred during login. Please try again.');
            }
        });
    }

    //  INDEX PAGE FUNCTIONALITY

    // Check if we're on the index page
    const placesList = document.getElementById('places-list');
    if (placesList) {
        checkAuthentication();
    }
});

// TASK INDEX PAGE FUNCTIONS

function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');

    if (!token) {
        // User is not authenticated - show login link
        if (loginLink) {
            loginLink.style.display = 'block';
        }
        // Still fetch places even if not authenticated (depends on your API requirements)
        fetchPlaces(null);
    } else {
        // User is authenticated - hide login link
        if (loginLink) {
            loginLink.style.display = 'none';
        }
        // Fetch places with authentication token
        fetchPlaces(token);
    }
}

async function fetchPlaces(token) {
    try {
        const headers = {
            'Content-Type': 'application/json'
        };

        // Add Authorization header if token exists
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        const response = await fetch(`${API_BASE_URL}/places`, {
            method: 'GET',
            headers: headers
        });

        if (response.ok) {
            const places = await response.json();
            displayPlaces(places);
            setupPriceFilter(places);
        } else {
            console.error('Failed to fetch places:', response.statusText);
            document.getElementById('places-list').innerHTML = '<p>Failed to load places. Please try again later.</p>';
        }
    } catch (error) {
        console.error('Error fetching places:', error);
        document.getElementById('places-list').innerHTML = '<p>An error occurred while loading places.</p>';
    }
}

function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    placesList.innerHTML = ''; // Clear existing content

    if (!places || places.length === 0) {
        placesList.innerHTML = '<p>No places available at the moment.</p>';
        return;
    }

    places.forEach(place => {
        const placeCard = document.createElement('div');
        placeCard.className = 'place-card';
        placeCard.setAttribute('data-price', place.price || 0);

        placeCard.innerHTML = `
            <img src="${place.image || 'images/placeholder.jpg'}" alt="${place.title}">
            <h3>${place.title}</h3>
            <p>Price per night: $${place.price || 'N/A'}</p>
            <p>${place.description ? place.description.substring(0, 100) + '...' : 'No description available'}</p>
            <button class="details-button" onclick="viewPlaceDetails('${place.id}')">View Details</button>
        `;

        placesList.appendChild(placeCard);
    });
}

function setupPriceFilter(places) {
    const priceFilter = document.getElementById('price-filter');
    
    if (priceFilter) {
        priceFilter.addEventListener('change', (event) => {
            const selectedPrice = event.target.value;
            filterPlacesByPrice(selectedPrice);
        });
    }
}

function filterPlacesByPrice(maxPrice) {
    const placeCards = document.querySelectorAll('.place-card');

    placeCards.forEach(card => {
        const price = parseFloat(card.getAttribute('data-price'));

        if (maxPrice === 'all') {
            card.style.display = 'block';
        } else {
            const max = parseFloat(maxPrice);
            if (price <= max) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        }
    });
}

function viewPlaceDetails(placeId) {
    window.location.href = `place.html?id=${placeId}`;
}

// TASK 3: PLACE DETAILS PAGE FUNCTIONS

function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('id');
}

async function fetchPlaceDetails(placeId, token) {
    try {
        const headers = {
            'Content-Type': 'application/json'
        };

        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        const response = await fetch(`${API_BASE_URL}/places/${placeId}`, {
            method: 'GET',
            headers: headers
        });

        if (response.ok) {
            const place = await response.json();
            displayPlaceDetails(place);
        } else {
            console.error('Failed to fetch place details:', response.statusText);
            document.getElementById('place-details').innerHTML = '<p>Failed to load place details. Please try again later.</p>';
        }
    } catch (error) {
        console.error('Error fetching place details:', error);
        document.getElementById('place-details').innerHTML = '<p>An error occurred while loading place details.</p>';
    }
}

function displayPlaceDetails(place) {
    const placeDetailsSection = document.getElementById('place-details');

    // Build amenities list
    let amenitiesHTML = '';
    if (place.amenities && place.amenities.length > 0) {
        amenitiesHTML = '<p><strong>Amenities:</strong> ' + place.amenities.map(a => a.name).join(', ') + '</p>';
    }

    // Build host information
    const hostName = place.owner ? `${place.owner.first_name} ${place.owner.last_name}` : 'Unknown';

    placeDetailsSection.innerHTML = `
        <div class="place-info">
            <h1>${place.title}</h1>
            <p><strong>Host:</strong> ${hostName}</p>
            <p><strong>Price:</strong> $${place.price} per night</p>
            <p><strong>Description:</strong> ${place.description || 'No description available'}</p>
            ${amenitiesHTML}
        </div>
    `;

    // Display reviews
    displayReviews(place.reviews || []);
}

function displayReviews(reviews) {
    const reviewsSection = document.getElementById('reviews');

    // Keep the h2 title
    let reviewsHTML = '<h2>Reviews</h2>';

    if (!reviews || reviews.length === 0) {
        reviewsHTML += '<p>No reviews yet.</p>';
    } else {
        reviews.forEach(review => {
            const userName = review.user ? `${review.user.first_name} ${review.user.last_name}` : 'Anonymous';
            const rating = '★'.repeat(review.rating) + '☆'.repeat(5 - review.rating);

            reviewsHTML += `
                <div class="review-card">
                    <strong>${userName}</strong>
                    <p>${review.text}</p>
                    <p>${rating}</p>
                </div>
            `;
        });
    }

    reviewsSection.innerHTML = reviewsHTML;
}

function checkAuthForReviews() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');
    const addReviewSection = document.getElementById('add-review');
    const placeId = getPlaceIdFromURL();

    if (!token) {
        // User not authenticated
        if (loginLink) loginLink.style.display = 'block';
        if (addReviewSection) addReviewSection.style.display = 'none';
        // Still fetch place details without token
        if (placeId) {
            fetchPlaceDetails(placeId, null);
        }
    } else {
        // User authenticated
        if (loginLink) loginLink.style.display = 'none';
        if (addReviewSection) addReviewSection.style.display = 'block';
        // Fetch place details with token
        if (placeId) {
            fetchPlaceDetails(placeId, token);
        }
    }
}

// Initialize place details page
document.addEventListener('DOMContentLoaded', () => {
    // Check if we're on the place details page
    const placeDetailsSection = document.getElementById('place-details');
    if (placeDetailsSection) {
        checkAuthForReviews();
        setupReviewFormSubmission();
    }

    // Check if we're on the add_review.html page
    const addReviewPage = document.getElementById('review-form');
    const isAddReviewPage = window.location.pathname.includes('add_review.html');
    if (addReviewPage && isAddReviewPage) {
        initializeAddReviewPage();
    }
});

function setupReviewFormSubmission() {
    const reviewForm = document.getElementById('review-form');

    if (reviewForm) {
        reviewForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const token = getCookie('token');
            if (!token) {
                alert('You must be logged in to submit a review.');
                window.location.href = 'login.html';
                return;
            }

            const placeId = getPlaceIdFromURL();
            const reviewText = document.getElementById('review-text').value;
            const rating = document.getElementById('rating').value;

            if (!reviewText || !rating) {
                alert('Please fill in all fields.');
                return;
            }

            try {
                const response = await fetch(`${API_BASE_URL}/reviews`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify({
                        place_id: placeId,
                        text: reviewText,
                        rating: parseInt(rating)
                    })
                });

                if (response.ok) {
                    alert('Review submitted successfully!');
                    // Reload the page to show the new review
                    window.location.reload();
                } else {
                    const errorData = await response.json();
                    alert('Failed to submit review: ' + (errorData.message || response.statusText));
                }
            } catch (error) {
                console.error('Error submitting review:', error);
                alert('An error occurred while submitting the review.');
            }
        });
    }
}

// TASK 4: ADD REVIEW PAGE FUNCTIONALITY

function initializeAddReviewPage() {
    // Check authentication
    const token = getCookie('token');
    if (!token) {
        // Redirect to index if not authenticated
        window.location.href = 'index.html';
        return;
    }

    const placeId = getPlaceIdFromURL();
    if (!placeId) {
        alert('No place ID provided.');
        window.location.href = 'index.html';
        return;
    }

    // Setup form submission for add_review.html page
    const reviewForm = document.getElementById('review-form');
    if (reviewForm) {
        reviewForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const reviewText = document.getElementById('review').value;
            const rating = document.getElementById('rating').value;

            if (!reviewText || !rating) {
                alert('Please fill in all fields.');
                return;
            }

            try {
                const response = await fetch(`${API_BASE_URL}/reviews`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify({
                        place_id: placeId,
                        text: reviewText,
                        rating: parseInt(rating)
                    })
                });

                if (response.ok) {
                    alert('Review submitted successfully!');
                    // Clear the form
                    reviewForm.reset();
                    // Redirect back to place details page
                    window.location.href = `place.html?id=${placeId}`;
                } else {
                    const errorData = await response.json();
                    alert('Failed to submit review: ' + (errorData.message || response.statusText));
                }
            } catch (error) {
                console.error('Error submitting review:', error);
                alert('An error occurred while submitting the review.');
            }
        });
    }
}
