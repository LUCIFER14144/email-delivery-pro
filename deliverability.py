import random
from datetime import datetime

class DeliverabilityAnalyzer:
    def __init__(self):
        self.major_providers = {
            'gmail.com': {'reputation_weight': 0.3, 'auth_weight': 0.4, 'content_weight': 0.3},
            'yahoo.com': {'reputation_weight': 0.4, 'auth_weight': 0.3, 'content_weight': 0.3},
            'outlook.com': {'reputation_weight': 0.25, 'auth_weight': 0.45, 'content_weight': 0.3},
            'apple.com': {'reputation_weight': 0.2, 'auth_weight': 0.5, 'content_weight': 0.3}
        }

    def analyze_domain_health(self, domain):
        health_data = {
            'domain': domain,
            'reputation_score': 0,
            'spf_status': 'unknown',
            'dkim_status': 'unknown', 
            'dmarc_status': 'unknown',
            'mx_records': [],
            'blacklist_status': 'clean',
            'ssl_cert_valid': False,
            'last_checked': datetime.utcnow(),
            'overall_health': 'unknown',
            'recommendations': []
        }

        try:
            # Simulate checks
            health_data['spf_status'] = self._simulate_spf_check(domain)
            health_data['dkim_status'] = self._simulate_dkim_check(domain)
            health_data['dmarc_status'] = self._simulate_dmarc_check(domain)
            health_data['mx_records'] = self._simulate_mx_records(domain)
            health_data['blacklist_status'] = self._simulate_blacklist_check(domain)
            health_data['reputation_score'] = self._calculate_reputation_score(health_data)
            health_data['overall_health'] = self._determine_overall_health(health_data)
            health_data['recommendations'] = self._generate_domain_recommendations(health_data)

        except Exception as e:
            health_data['error'] = str(e)

        return health_data

    def _simulate_spf_check(self, domain):
        # Simulate SPF record check
        chance = random.random()
        if chance < 0.7:
            return 'valid'
        elif chance < 0.85:
            return 'basic'
        else:
            return 'missing'

    def _simulate_dkim_check(self, domain):
        # Simulate DKIM check
        chance = random.random()
        if chance < 0.6:
            return 'valid'
        elif chance < 0.8:
            return 'partial'
        else:
            return 'missing'

    def _simulate_dmarc_check(self, domain):
        # Simulate DMARC check
        chance = random.random()
        if chance < 0.3:
            return 'strict'
        elif chance < 0.5:
            return 'moderate'
        elif chance < 0.7:
            return 'monitor'
        elif chance < 0.85:
            return 'basic'
        else:
            return 'missing'

    def _simulate_mx_records(self, domain):
        # Simulate MX records
        return [
            {'priority': 10, 'exchange': f'mail.{domain}'},
            {'priority': 20, 'exchange': f'mail2.{domain}'}
        ]

    def _simulate_blacklist_check(self, domain):
        # Simulate blacklist check
        chance = random.random()
        if chance < 0.05:
            return 'blacklisted'
        elif chance < 0.15:
            return 'warning'
        else:
            return 'clean'

    def _calculate_reputation_score(self, health_data):
        score = 50  # Base score

        # SPF bonus/penalty
        if health_data['spf_status'] == 'valid':
            score += 20
        elif health_data['spf_status'] == 'basic':
            score += 10
        else:
            score -= 15

        # DKIM bonus/penalty
        if health_data['dkim_status'] == 'valid':
            score += 15
        elif health_data['dkim_status'] == 'partial':
            score += 8
        else:
            score -= 10

        # DMARC bonus/penalty
        if health_data['dmarc_status'] == 'strict':
            score += 15
        elif health_data['dmarc_status'] in ['moderate', 'monitor']:
            score += 10
        elif health_data['dmarc_status'] == 'basic':
            score += 5
        else:
            score -= 10

        # Blacklist penalty
        if health_data['blacklist_status'] == 'blacklisted':
            score -= 30
        elif health_data['blacklist_status'] == 'warning':
            score -= 10

        # MX records bonus
        if len(health_data['mx_records']) > 0:
            score += 5

        return max(0, min(100, score))

    def _determine_overall_health(self, health_data):
        score = health_data['reputation_score']

        if score >= 85:
            return 'excellent'
        elif score >= 70:
            return 'good'
        elif score >= 50:
            return 'fair'
        else:
            return 'poor'

    def _generate_domain_recommendations(self, health_data):
        recommendations = []

        if health_data['spf_status'] == 'missing':
            recommendations.append({
                'priority': 'high',
                'category': 'Authentication',
                'title': 'Add SPF Record',
                'description': 'Configure SPF record to authorize sending servers',
                'action': f'Add TXT record: "v=spf1 include:_spf.google.com ~all" for {health_data["domain"]}'
            })

        if health_data['dkim_status'] == 'missing':
            recommendations.append({
                'priority': 'high',
                'category': 'Authentication',
                'title': 'Enable DKIM Signing',
                'description': 'Set up DKIM to cryptographically sign your emails',
                'action': 'Configure DKIM keys with your email service provider'
            })

        if health_data['dmarc_status'] == 'missing':
            recommendations.append({
                'priority': 'medium',
                'category': 'Authentication', 
                'title': 'Implement DMARC Policy',
                'description': 'Add DMARC record for email authentication policy',
                'action': f'Add TXT record for _dmarc.{health_data["domain"]}: "v=DMARC1; p=quarantine; rua=mailto:dmarc@{health_data["domain"]}"'
            })

        if health_data['blacklist_status'] == 'blacklisted':
            recommendations.append({
                'priority': 'critical',
                'category': 'Reputation',
                'title': 'Address Blacklisting',
                'description': 'Your domain appears on email blacklists',
                'action': 'Contact blacklist operators for removal and improve sending practices'
            })

        return recommendations
