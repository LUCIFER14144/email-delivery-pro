# 13. Create templates/spam_checker.html
spam_checker_template = '''{% extends "base.html" %}

{% block content %}
<div class="container py-4">
    <div class="row">
        <div class="col-lg-8 mx-auto">
            <div class="text-center mb-4">
                <h1 class="h3">
                    <i class="fas fa-shield-alt text-primary"></i>
                    Email Spam Score Checker
                </h1>
                <p class="text-muted">
                    Analyze your email content for spam triggers and get actionable recommendations
                </p>
            </div>

            <div class="card shadow">
                <div class="card-body p-4">
                    <form method="POST" id="spam-checker-form">
                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <label for="subject" class="form-label">
                                    <i class="fas fa-heading"></i> Subject Line *
                                </label>
                                <input type="text" 
                                       class="form-control" 
                                       id="subject" 
                                       name="subject" 
                                       placeholder="Enter your email subject line"
                                       required
                                       maxlength="255">
                                <div class="form-text">Keep it under 50 characters for best results</div>
                            </div>

                            <div class="col-md-6 mb-3">
                                <label for="sender_email" class="form-label">
                                    <i class="fas fa-envelope"></i> From Email *
                                </label>
                                <input type="email" 
                                       class="form-control" 
                                       id="sender_email" 
                                       name="sender_email" 
                                       placeholder="sender@yourdomain.com"
                                       required>
                                <div class="form-text">The email address you're sending from</div>
                            </div>
                        </div>

                        <div class="mb-3">
                            <label for="html_content" class="form-label">
                                <i class="fas fa-code"></i> Email Content (HTML) *
                            </label>
                            <textarea class="form-control" 
                                      id="html_content" 
                                      name="html_content" 
                                      rows="12" 
                                      placeholder="Paste your HTML email content here..."
                                      required></textarea>
                            <div class="form-text">
                                Include your complete HTML email template. 
                                <a href="#" onclick="loadSampleEmail()">Load sample email</a>
                            </div>
                        </div>

                        <div class="mb-4">
                            <label for="text_content" class="form-label">
                                <i class="fas fa-align-left"></i> Plain Text Version (Optional)
                            </label>
                            <textarea class="form-control" 
                                      id="text_content" 
                                      name="text_content" 
                                      rows="6" 
                                      placeholder="Plain text version of your email (optional but recommended)"></textarea>
                        </div>

                        <div class="d-grid">
                            <button type="submit" class="btn btn-primary btn-lg">
                                <i class="fas fa-search"></i>
                                Analyze Email for Spam Risk
                            </button>
                        </div>
                    </form>
                </div>
            </div>

            <!-- Tips Section -->
            <div class="card mt-4">
                <div class="card-header">
                    <h5 class="mb-0">
                        <i class="fas fa-lightbulb text-warning"></i>
                        Tips for Better Deliverability
                    </h5>
                </div>
                <div class="card-body">
                    <div class="row">
                        <div class="col-md-6">
                            <h6><i class="fas fa-check text-success"></i> Do:</h6>
                            <ul class="list-unstyled">
                                <li>• Use a clear, descriptive subject line</li>
                                <li>• Include both HTML and plain text versions</li>
                                <li>• Maintain good text-to-image ratio</li>
                                <li>• Use proper SPF/DKIM authentication</li>
                                <li>• Include an easy unsubscribe option</li>
                            </ul>
                        </div>
                        <div class="col-md-6">
                            <h6><i class="fas fa-times text-danger"></i> Avoid:</h6>
                            <ul class="list-unstyled">
                                <li>• ALL CAPS subject lines</li>
                                <li>• Excessive exclamation marks!!!</li>
                                <li>• Spam trigger words (FREE, URGENT, etc.)</li>
                                <li>• Too many images, not enough text</li>
                                <li>• Hidden or misleading content</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

{% endblock %}

{% block scripts %}
<script>
function loadSampleEmail() {
    const sampleHTML = `<!DOCTYPE html>
<html>
<head>
    <title>Weekly Newsletter</title>
</head>
<body>
    <div style="max-width: 600px; margin: 0 auto; font-family: Arial, sans-serif;">
        <h1 style="color: #333; text-align: center;">Welcome to Our Newsletter</h1>
        
        <p>Dear Subscriber,</p>
        
        <p>Thank you for subscribing to our weekly newsletter. Here are this week's highlights:</p>
        
        <ul>
            <li>New product launches</li>
            <li>Industry insights</li>
            <li>Special offers for subscribers</li>
        </ul>
        
        <p>Best regards,<br>The Team</p>
        
        <hr style="margin: 30px 0;">
        
        <p style="font-size: 12px; color: #666; text-align: center;">
            If you no longer wish to receive these emails, you can 
            <a href="#">unsubscribe here</a>.
        </p>
    </div>
</body>
</html>`;

    document.getElementById('html_content').value = sampleHTML;
    document.getElementById('subject').value = 'Weekly Newsletter - October Edition';
    document.getElementById('sender_email').value = 'newsletter@yourcompany.com';
}
</script>
{% endblock %}'''

with open(f"{project_name}/templates/spam_checker.html", 'w') as f:
    f.write(spam_checker_template)

print("✅ templates/spam_checker.html created")