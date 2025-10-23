# 10. Create templates/landing.html
landing_template = '''{% extends "base.html" %}

{% block content %}
<!-- Hero Section -->
<section class="hero-section bg-gradient-primary text-white py-5">
    <div class="container">
        <div class="row align-items-center">
            <div class="col-lg-6">
                <h1 class="display-4 fw-bold mb-4">
                    Achieve 90% Inbox Delivery Rates
                </h1>
                <p class="lead mb-4">
                    Professional email deliverability testing and optimization tools. 
                    Stop landing in spam folders and maximize your email marketing ROI.
                </p>
                <div class="d-flex gap-3">
                    <a href="{{ url_for('register') }}" class="btn btn-light btn-lg">
                        Start Free Trial
                    </a>
                    <a href="#features" class="btn btn-outline-light btn-lg">
                        Learn More
                    </a>
                </div>
                <div class="mt-4">
                    <small>
                        <i class="fas fa-check text-success"></i> No credit card required
                        &nbsp;&nbsp;
                        <i class="fas fa-check text-success"></i> Free 14-day trial
                    </small>
                </div>
            </div>
            <div class="col-lg-6">
                <div class="hero-dashboard">
                    <img src="https://via.placeholder.com/600x400/007bff/ffffff?text=Dashboard+Preview" 
                         class="img-fluid rounded shadow" alt="Dashboard Preview">
                </div>
            </div>
        </div>
    </div>
</section>

<!-- Features Section -->
<section id="features" class="py-5">
    <div class="container">
        <div class="text-center mb-5">
            <h2 class="display-5 fw-bold">Why Choose Email Deliverability Pro?</h2>
            <p class="lead text-muted">Comprehensive tools to optimize your email campaigns</p>
        </div>
        
        <div class="row">
            <div class="col-md-4 mb-4">
                <div class="feature-card text-center p-4">
                    <div class="feature-icon mb-3">
                        <i class="fas fa-shield-alt fa-3x text-primary"></i>
                    </div>
                    <h4>Spam Score Analysis</h4>
                    <p class="text-muted">
                        Get detailed spam score analysis with actionable recommendations 
                        to improve your email content and avoid spam filters.
                    </p>
                </div>
            </div>
            
            <div class="col-md-4 mb-4">
                <div class="feature-card text-center p-4">
                    <div class="feature-icon mb-3">
                        <i class="fas fa-inbox fa-3x text-success"></i>
                    </div>
                    <h4>Inbox Placement Testing</h4>
                    <p class="text-muted">
                        Test where your emails land across Gmail, Yahoo, Outlook, and Apple Mail. 
                        See real inbox placement rates before sending.
                    </p>
                </div>
            </div>
            
            <div class="col-md-4 mb-4">
                <div class="feature-card text-center p-4">
                    <div class="feature-icon mb-3">
                        <i class="fas fa-globe fa-3x text-info"></i>
                    </div>
                    <h4>Domain Health Monitoring</h4>
                    <p class="text-muted">
                        Monitor your domain's reputation, SPF/DKIM/DMARC configuration, 
                        and blacklist status in real-time.
                    </p>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- Pricing Section -->
<section class="py-5 bg-light">
    <div class="container">
        <div class="text-center mb-5">
            <h2 class="display-5 fw-bold">Simple, Transparent Pricing</h2>
            <p class="lead text-muted">Choose the plan that fits your needs</p>
        </div>
        
        <div class="row justify-content-center">
            {% for plan_id, plan in plans.items() %}
            <div class="col-lg-4 col-md-6 mb-4">
                <div class="pricing-card card h-100 {% if plan_id == 'professional' %}border-primary{% endif %}">
                    {% if plan_id == 'professional' %}
                    <div class="card-header bg-primary text-white text-center">
                        <small>Most Popular</small>
                    </div>
                    {% endif %}
                    
                    <div class="card-body text-center">
                        <h4 class="card-title">{{ plan.name }}</h4>
                        <div class="pricing-amount mb-3">
                            <span class="display-4 fw-bold">${{ plan.price }}</span>
                            <small class="text-muted">/month</small>
                        </div>
                        
                        <ul class="list-unstyled">
                            {% if plan.max_domains == -1 %}
                            <li><i class="fas fa-check text-success"></i> Unlimited domains</li>
                            {% else %}
                            <li><i class="fas fa-check text-success"></i> {{ plan.max_domains }} domains</li>
                            {% endif %}
                            
                            {% if plan.max_tests_per_month == -1 %}
                            <li><i class="fas fa-check text-success"></i> Unlimited tests</li>
                            {% else %}
                            <li><i class="fas fa-check text-success"></i> {{ plan.max_tests_per_month }} tests/month</li>
                            {% endif %}
                            
                            {% for feature in plan.features %}
                            <li><i class="fas fa-check text-success"></i> {{ feature }}</li>
                            {% endfor %}
                        </ul>
                        
                        <a href="{{ url_for('register') }}" 
                           class="btn {% if plan_id == 'professional' %}btn-primary{% else %}btn-outline-primary{% endif %} btn-lg w-100">
                            Get Started
                        </a>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>
</section>

<!-- Stats Section -->
<section class="py-5">
    <div class="container">
        <div class="row text-center">
            <div class="col-md-3 mb-4">
                <div class="stat-item">
                    <h2 class="display-4 text-primary fw-bold">92%</h2>
                    <p class="lead">Average Delivery Rate</p>
                </div>
            </div>
            <div class="col-md-3 mb-4">
                <div class="stat-item">
                    <h2 class="display-4 text-success fw-bold">10,000+</h2>
                    <p class="lead">Emails Tested Daily</p>
                </div>
            </div>
            <div class="col-md-3 mb-4">
                <div class="stat-item">
                    <h2 class="display-4 text-info fw-bold">500+</h2>
                    <p class="lead">Happy Customers</p>
                </div>
            </div>
            <div class="col-md-3 mb-4">
                <div class="stat-item">
                    <h2 class="display-4 text-warning fw-bold">24/7</h2>
                    <p class="lead">Monitoring</p>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- CTA Section -->
<section class="py-5 bg-primary text-white">
    <div class="container text-center">
        <h2 class="display-5 fw-bold mb-3">Ready to Improve Your Email Deliverability?</h2>
        <p class="lead mb-4">Join hundreds of businesses achieving 90%+ inbox delivery rates</p>
        <a href="{{ url_for('register') }}" class="btn btn-light btn-lg">
            Start Your Free Trial Today
        </a>
    </div>
</section>
{% endblock %}'''

with open(f"{project_name}/templates/landing.html", 'w') as f:
    f.write(landing_template)

print("✅ templates/landing.html created")