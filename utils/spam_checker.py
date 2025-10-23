import re
import random

class SpamChecker:
    def __init__(self):
        self.spam_keywords = {
            'high_risk': ['FREE', 'URGENT', 'ACT NOW', 'LIMITED TIME', 'GUARANTEED', 'WINNER', 'CONGRATULATIONS'],
            'medium_risk': ['DEAL', 'SAVE', 'DISCOUNT', 'SPECIAL', 'OFFER', 'BUY NOW', 'CLICK HERE'],
            'low_risk': ['SALE', 'NEW', 'AVAILABLE', 'NEWSLETTER', 'UPDATE']
        }

        self.suspicious_patterns = [
            r'(\$\d+)',          # Dollar amounts
            r'(\d+%\s*off)',     # Percentage discounts
            r'(free\s*trial)',    # Free trials
            r'(no\s*cost)',       # No cost
            r'(risk\s*free)',     # Risk free
        ]

    def check_content(self, subject, html_content, text_content=""):
        results = {
            'spam_score': 0,
            'risk_level': 'low',
            'issues': [],
            'keyword_analysis': {},
            'pattern_analysis': {},
            'recommendations': []
        }

        full_content = f"{subject} {html_content} {text_content}".upper()

        # Check spam keywords
        keyword_results = self._check_keywords(full_content)
        results['keyword_analysis'] = keyword_results
        results['spam_score'] += keyword_results['score']

        # Check suspicious patterns
        pattern_results = self._check_patterns(full_content)
        results['pattern_analysis'] = pattern_results
        results['spam_score'] += pattern_results['score']

        # Check HTML structure
        html_results = self._analyze_html(html_content)
        results['spam_score'] += html_results['score']
        results['issues'].extend(html_results['issues'])

        # Check subject line
        subject_results = self._analyze_subject(subject)
        results['spam_score'] += subject_results['score']
        results['issues'].extend(subject_results['issues'])

        # Determine risk level
        if results['spam_score'] <= 20:
            results['risk_level'] = 'low'
        elif results['spam_score'] <= 50:
            results['risk_level'] = 'medium'
        else:
            results['risk_level'] = 'high'

        # Generate recommendations
        results['recommendations'] = self._generate_spam_recommendations(results)

        return results

    def _check_keywords(self, content):
        found_keywords = {'high_risk': [], 'medium_risk': [], 'low_risk': []}
        score = 0

        for risk_level, keywords in self.spam_keywords.items():
            for keyword in keywords:
                if keyword in content:
                    found_keywords[risk_level].append(keyword)
                    if risk_level == 'high_risk':
                        score += 15
                    elif risk_level == 'medium_risk':
                        score += 8
                    else:
                        score += 3

        return {
            'found_keywords': found_keywords,
            'score': score
        }

    def _check_patterns(self, content):
        found_patterns = []
        score = 0

        for pattern in self.suspicious_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                found_patterns.extend(matches)
                score += len(matches) * 5

        return {
            'found_patterns': found_patterns,
            'score': score
        }

    def _analyze_html(self, html_content):
        issues = []
        score = 0

        if not html_content:
            return {'score': 0, 'issues': []}

        # Check for excessive links
        links = re.findall(r'<a[^>]*href', html_content, re.IGNORECASE)
        if len(links) > 10:
            issues.append(f"Too many links detected ({len(links)})")
            score += 10

        # Check for hidden text patterns
        hidden_text_patterns = [
            r'color:\s*white[^;]*background:\s*white',
            r'color:\s*#ffffff[^;]*background:\s*#ffffff',
            r'font-size:\s*0',
            r'display:\s*none'
        ]

        for pattern in hidden_text_patterns:
            if re.search(pattern, html_content, re.IGNORECASE):
                issues.append("Potential hidden text detected")
                score += 20
                break

        # Check for excessive capitalization
        if html_content.upper() == html_content and len(html_content) > 100:
            issues.append("Excessive use of capital letters")
            score += 15

        # Check image to text ratio
        img_count = len(re.findall(r'<img', html_content, re.IGNORECASE))
        text_content = re.sub(r'<[^>]+>', '', html_content)
        text_length = len(text_content.strip())

        if img_count > 0 and text_length < 100:
            issues.append("Image-heavy content with little text")
            score += 12

        return {
            'score': score,
            'issues': issues
        }

    def _analyze_subject(self, subject):
        issues = []
        score = 0

        # Check length
        if len(subject) > 60:
            issues.append("Subject line is too long")
            score += 8
        elif len(subject) < 10:
            issues.append("Subject line is too short")
            score += 5

        # Check for excessive punctuation
        punctuation_count = len(re.findall(r'[!?]', subject))
        if punctuation_count > 2:
            issues.append("Excessive punctuation in subject")
            score += 10

        # Check for all caps
        if subject.isupper() and len(subject) > 10:
            issues.append("Subject line is in all capitals")
            score += 15

        # Check for numbers at start
        if re.match(r'^\d+', subject):
            issues.append("Subject starts with numbers")
            score += 5

        return {
            'score': score,
            'issues': issues
        }

    def _generate_spam_recommendations(self, results):
        recommendations = []

        if results['spam_score'] > 50:
            recommendations.append("⚠️ High spam risk detected - major changes needed")
        elif results['spam_score'] > 20:
            recommendations.append("⚡ Moderate spam risk - some improvements recommended")
        else:
            recommendations.append("✅ Low spam risk - content looks good!")

        # Add specific recommendations based on issues
        for issue in results['issues']:
            if "links" in issue.lower():
                recommendations.append("Reduce the number of links in your email")
            elif "hidden" in issue.lower():
                recommendations.append("Remove any hidden text or styling")
            elif "capital" in issue.lower():
                recommendations.append("Use normal capitalization instead of ALL CAPS")
            elif "image-heavy" in issue.lower():
                recommendations.append("Add more text content and reduce images")
            elif "subject" in issue.lower() and "long" in issue.lower():
                recommendations.append("Shorten your subject line to under 50 characters")

        return recommendations
