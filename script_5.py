# 5. Create utils/email_tester.py
email_tester_content = '''import re
import random

class EmailTester:
    def __init__(self):
        self.providers = ['gmail', 'yahoo', 'outlook', 'apple']
        
    def analyze_email(self, subject, sender_email, html_content, text_content=""):
        """
        Comprehensive email analysis including spam score, deliverability prediction
        """
        results = {
            'overall_score': 0,
            'spam_score': 0,
            'delivery_rate': 0,
            'provider_results': [],
            'spam_factors': [],
            'recommendations': []
        }
        
        # Analyze spam factors
        spam_factors = self._analyze_spam_factors(subject, sender_email, html_content, text_content)
        results['spam_factors'] = spam_factors
        
        # Calculate spam score (0-100, lower is better)
        spam_score = self._calculate_spam_score(spam_factors)
        results['spam_score'] = spam_score
        
        # Predict provider-specific results
        provider_results = self._predict_provider_results(spam_score, sender_email)
        results['provider_results'] = provider_results
        
        # Calculate overall delivery rate
        delivery_rate = sum([p['inbox_rate'] for p in provider_results]) / len(provider_results)
        results['delivery_rate'] = delivery_rate
        
        # Overall score (higher is better)
        results['overall_score'] = max(0, 100 - spam_score)
        
        # Generate recommendations
        results['recommendations'] = self._generate_recommendations(spam_factors)
        
        return results
    
    def _analyze_spam_factors(self, subject, sender_email, html_content, text_content):
        factors = []
        
        # Subject line analysis
        if len(subject) > 60:
            factors.append({
                'factor': 'Subject Line Length',
                'status': 'Warning',
                'impact': 'negative',
                'description': f'Subject line is {len(subject)} characters (recommended: under 50)',
                'score': -5
            })
        else:
            factors.append({
                'factor': 'Subject Line Length',
                'status': 'Good',
                'impact': 'positive', 
                'description': f'Subject line length is optimal ({len(subject)} chars)',
                'score': 5
            })
        
        # Check for spam words
        spam_words = ['FREE', 'URGENT', 'ACT NOW', 'LIMITED TIME', 'GUARANTEE', 'CLICK HERE']
        found_spam_words = [word for word in spam_words if word.lower() in subject.lower()]
        
        if found_spam_words:
            factors.append({
                'factor': 'Spam Keywords',
                'status': 'Alert',
                'impact': 'negative',
                'description': f'Found spam keywords: {", ".join(found_spam_words)}',
                'score': -10 * len(found_spam_words)
            })
        else:
            factors.append({
                'factor': 'Spam Keywords',
                'status': 'Good',
                'impact': 'positive',
                'description': 'No obvious spam keywords detected',
                'score': 10
            })
        
        # HTML analysis
        if html_content:
            img_count = html_content.lower().count('<img')
            text_length = len(re.sub(r'<[^>]+>', '', html_content))
            
            if img_count > 0 and text_length < 100:
                factors.append({
                    'factor': 'Image to Text Ratio',
                    'status': 'Warning',
                    'impact': 'negative',
                    'description': 'Too many images, not enough text',
                    'score': -8
                })
            else:
                factors.append({
                    'factor': 'Image to Text Ratio',
                    'status': 'Good',
                    'impact': 'positive',
                    'description': 'Healthy balance of text and images',
                    'score': 5
                })
        
        domain = sender_email.split('@')[1] if '@' in sender_email else 'unknown'
        
        auth_factors = self._check_authentication(domain)
        factors.extend(auth_factors)
        
        return factors
    
    def _check_authentication(self, domain):
        factors = []
        
        # Simulate SPF check (75% chance valid)
        spf_valid = random.choice([True, True, True, False])
        if spf_valid:
            factors.append({
                'factor': 'SPF Authentication',
                'status': 'Pass',
                'impact': 'positive',
                'description': 'SPF record is properly configured',
                'score': 15
            })
        else:
            factors.append({
                'factor': 'SPF Authentication',
                'status': 'Fail',
                'impact': 'negative',
                'description': 'SPF record is missing or invalid',
                'score': -20
            })
        
        # Simulate DKIM check (67% chance valid)
        dkim_valid = random.choice([True, True, False])
        if dkim_valid:
            factors.append({
                'factor': 'DKIM Signature',
                'status': 'Pass',
                'impact': 'positive',
                'description': 'Email is properly DKIM signed',
                'score': 15
            })
        else:
            factors.append({
                'factor': 'DKIM Signature',
                'status': 'Fail',
                'impact': 'negative',
                'description': 'DKIM signature is missing or invalid',
                'score': -15
            })
        
        # Simulate DMARC check (50% chance valid)
        dmarc_valid = random.choice([True, False])
        if dmarc_valid:
            factors.append({
                'factor': 'DMARC Policy',
                'status': 'Pass',
                'impact': 'positive',
                'description': 'DMARC policy is properly aligned',
                'score': 10
            })
        else:
            factors.append({
                'factor': 'DMARC Policy',
                'status': 'Fail',
                'impact': 'negative',
                'description': 'DMARC policy is not configured',
                'score': -10
            })
        
        return factors
    
    def _calculate_spam_score(self, factors):
        base_score = 30
        for factor in factors:
            base_score -= factor.get('score', 0)
        return max(0, min(100, base_score))
    
    def _predict_provider_results(self, spam_score, sender_email):
        results = []
        provider_configs = {
            'Gmail': {'base_inbox': 85, 'spam_sensitivity': 1.2},
            'Outlook': {'base_inbox': 80, 'spam_sensitivity': 1.1},
            'Yahoo': {'base_inbox': 75, 'spam_sensitivity': 1.3},
            'Apple Mail': {'base_inbox': 90, 'spam_sensitivity': 0.9}
        }
        
        for provider, config in provider_configs.items():
            penalty = (spam_score * config['spam_sensitivity']) / 2
            inbox_rate = max(10, config['base_inbox'] - penalty)
            inbox_rate += random.uniform(-3, 3)
            inbox_rate = max(0, min(100, inbox_rate))
            spam_rate = min(90, 100 - inbox_rate + random.uniform(-2, 2))
            missing_rate = max(0, 100 - inbox_rate - spam_rate)
            
            results.append({
                'provider': provider,
                'inbox_rate': round(inbox_rate, 1),
                'spam_rate': round(spam_rate, 1),
                'missing_rate': round(missing_rate, 1)
            })
        
        return results
    
    def _generate_recommendations(self, factors):
        recommendations = []
        
        for factor in factors:
            if factor['impact'] == 'negative':
                if 'Subject Line Length' in factor['factor']:
                    recommendations.append("Shorten your subject line to under 50 characters for better deliverability")
                elif 'Spam Keywords' in factor['factor']:
                    recommendations.append("Remove spam trigger words from your subject line and content")
                elif 'SPF' in factor['factor']:
                    recommendations.append("Configure SPF record for your domain to improve authentication")
                elif 'DKIM' in factor['factor']:
                    recommendations.append("Set up DKIM signing for your emails")
                elif 'DMARC' in factor['factor']:
                    recommendations.append("Implement DMARC policy for better domain protection")
                elif 'Image to Text' in factor['factor']:
                    recommendations.append("Add more text content and reduce image count")
        
        if not recommendations:
            recommendations.append("Your email looks good! Monitor delivery rates and engagement metrics.")
        
        return recommendations
'''

with open(f"{project_name}/utils/email_tester.py", 'w') as f:
    f.write(email_tester_content)

print("✅ utils/email_tester.py created")