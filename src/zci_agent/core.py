import random

class ZCIAgent:
    """
    Zohar Commerce Intelligence (ZCI) Agent.
    Responsible for generating high-converting product descriptions and optimizing SEO content.
    """

    def __init__(self):
        pass

    def generate_description(self, product_name, attributes):
        """
        Generates a creative product description based on product name and attributes.
        """
        if not product_name:
            return "Please provide a product name."
        
        attr_str = ", ".join(attributes) if attributes else "amazing features"
        
        # Simple template-based generation for now.
        # In a real scenario, this would connect to an LLM.
        templates = [
            f"Experience the magic of {product_name}. Designed with {attr_str}, it transforms your daily routine into a luxury experience.",
            f"Discover {product_name}, the ultimate choice for those who value {attr_str}. Elevate your style today.",
            f"Introducing {product_name}. With {attr_str}, it's everything you've been looking for and more."
        ]
        
        return random.choice(templates)

    def optimize_seo(self, text, keywords):
        """
        Optimizes the given text by ensuring keywords are present naturally.
        """
        if not text:
            return ""
        
        if not keywords:
            return text

        optimized_text = text
        missing_keywords = []

        for keyword in keywords:
            if keyword.lower() not in text.lower():
                missing_keywords.append(keyword)
        
        if missing_keywords:
            keyword_str = ", ".join(missing_keywords)
            optimized_text += f" Perfect for those interested in {keyword_str}."
            
        return optimized_text

    def validate_content(self, text):
        """
        Basic quality check for the generated content.
        """
        if not text:
            return False, "Content is empty."
        
        if len(text) < 20:
            return False, "Content is too short."
            
        return True, "Content looks good."
