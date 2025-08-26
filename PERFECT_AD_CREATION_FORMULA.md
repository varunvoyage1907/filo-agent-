# 🎯 PERFECT AD CREATION FORMULA

## 📋 OVERVIEW
This document contains the **exact formula** for creating perfect Facebook Advantage+ catalog ads. Only the **headline** and **primary text** should be changed. Everything else remains identical.

---

## 🔧 TECHNICAL SETUP (NEVER CHANGE)

### Required Parameters:
```python
access_token = 'YOUR_CURRENT_TOKEN'
account_id = 'act_612972137428654'
adset_id = '120233161126020134'  # Your existing ad set with Ray-Ban & Oakley targeting
product_set_id = '28436700479311981'  # Your GoEye product catalog
```

### Fixed Creative Structure:
```python
object_story_spec = {
    'page_id': '115963897786512',
    'instagram_user_id': '17841452313877305',
    'template_data': {
        'link': 'https://goeye.in/collections/all',
        'message': PRIMARY_TEXT,  # ← ONLY CHANGE THIS
        'name': HEADLINE,         # ← ONLY CHANGE THIS
        'call_to_action': {'type': 'SHOP_NOW'},
        'format_option': 'carousel_images_multi_items',
        'image_layer_specs': [
            {'image_source': 'catalog', 'layer_type': 'image'},
            {
                'blending_mode': 'normal',
                'frame_auto_show_enroll_status': 'OPT_OUT',
                'frame_image_hash': '4cd3b7b0cf72f0c1e6101f2449436e65',
                'frame_source': 'custom',
                'layer_type': 'frame_overlay',
                'opacity': 100,
                'overlay_position': 'center',
                'scale': 100
            }
        ],
        'multi_share_end_card': False,
        'automated_product_tags': True
    }
}
```

---

## ✍️ CONTENT CREATION RULES

### 🎯 HEADLINE GUIDELINES:
1. **Keep it benefit-focused** (not feature-focused)
2. **Include FREE prescription lenses** (your key differentiator)
3. **Add urgency/intrigue** ("Inside!", "Limited Time", etc.)
4. **NO product variables** (no {{product.name}} or {{product.price}})
5. **Keep under 40 characters** for mobile optimization

**✅ GOOD EXAMPLES:**
- "Premium Eyewear + FREE Prescription Lenses Inside!"
- "FREE Prescription Lenses + Designer Frames!"
- "Limited Time: FREE Lenses with Every Frame!"

**❌ AVOID:**
- Using {{product.current_price}} or {{product.name}} in headlines
- Price-focused headlines ("Starting at ₹999")
- Generic headlines ("Buy Eyewear Now")

### 📄 PRIMARY TEXT GUIDELINES:

#### Structure Template:
```
🔥 [ATTENTION GRABBER]: [MAIN BENEFIT]

👓 [EMOTIONAL HOOK]
✨ What makes this deal incredible:
• [BENEFIT 1]
• [BENEFIT 2 - FREE prescription lenses]
• [BENEFIT 3 - Existing offers]
• [BENEFIT 4 - Additional value]

💎 Why customers love us:
→ [SOCIAL PROOF 1]
→ [SOCIAL PROOF 2]
→ [SOCIAL PROOF 3]
→ [SOCIAL PROOF 4]

⚡ [URGENCY STATEMENT]
👆 [CLEAR CALL TO ACTION]
```

#### Content Rules:
1. **NO product variables** in primary text
2. **Always include FREE prescription lenses** as key benefit
3. **Maintain existing offers** (₹150 OFF + BOGO 50%)
4. **Use emojis** for visual appeal
5. **Include social proof** (customer count, guarantees)
6. **Create urgency** without pressure
7. **End with clear CTA**

---

## 🚀 COMPLETE CREATION SCRIPT

```python
import requests
import json

def create_perfect_ad(headline, primary_text, ad_name):
    """
    Creates a perfect Advantage+ catalog ad with only headline and primary text changes
    """
    
    # FIXED PARAMETERS (NEVER CHANGE)
    access_token = 'YOUR_CURRENT_TOKEN'
    account_id = 'act_612972137428654'
    adset_id = '120233161126020134'
    product_set_id = '28436700479311981'
    
    print(f'🚀 Creating perfect ad: {ad_name}')
    
    # FIXED CREATIVE STRUCTURE
    object_story_spec = {
        'page_id': '115963897786512',
        'instagram_user_id': '17841452313877305',
        'template_data': {
            'link': 'https://goeye.in/collections/all',
            'message': primary_text,  # ← ONLY VARIABLE
            'name': headline,         # ← ONLY VARIABLE
            'call_to_action': {'type': 'SHOP_NOW'},
            'format_option': 'carousel_images_multi_items',
            'image_layer_specs': [
                {'image_source': 'catalog', 'layer_type': 'image'},
                {
                    'blending_mode': 'normal',
                    'frame_auto_show_enroll_status': 'OPT_OUT',
                    'frame_image_hash': '4cd3b7b0cf72f0c1e6101f2449436e65',
                    'frame_source': 'custom',
                    'layer_type': 'frame_overlay',
                    'opacity': 100,
                    'overlay_position': 'center',
                    'scale': 100
                }
            ],
            'multi_share_end_card': False,
            'automated_product_tags': True
        }
    }
    
    # Step 1: Create Creative
    creative_response = requests.post(f'https://graph.facebook.com/v19.0/{account_id}/adcreatives', data={
        'access_token': access_token,
        'name': f'{ad_name} - Creative',
        'object_story_spec': json.dumps(object_story_spec),
        'product_set_id': product_set_id
    })
    
    if creative_response.status_code == 200:
        creative_id = creative_response.json().get('id')
        print(f'✅ Creative: {creative_id}')
        
        # Step 2: Create Ad
        ad_response = requests.post(f'https://graph.facebook.com/v19.0/{account_id}/ads', data={
            'access_token': access_token,
            'name': ad_name,
            'adset_id': adset_id,
            'creative': json.dumps({'creative_id': creative_id}),
            'status': 'ACTIVE'
        })
        
        if ad_response.status_code == 200:
            ad_id = ad_response.json().get('id')
            print(f'🎉 SUCCESS! AD CREATED: {ad_id}')
            return ad_id, creative_id
        else:
            print(f'❌ Ad creation failed: {ad_response.status_code}')
    else:
        print(f'❌ Creative creation failed: {creative_response.status_code}')
    
    return None, None

# USAGE EXAMPLE:
headline = "Premium Eyewear + FREE Prescription Lenses Inside!"
primary_text = '''🔥 EXCLUSIVE: Get FREE Prescription Lenses with Every Frame!

👓 Transform your vision AND style with premium eyewear
✨ What makes this deal incredible:
• Choose from 1000+ premium frame styles
• Get prescription lenses absolutely FREE with every purchase
• Buy 1 frame → Save ₹150 instantly
• Buy 2 frames → Get 50% OFF the second frame

💎 Why customers love us:
→ Premium quality frames that last for years
→ Perfect fit guarantee or full refund
→ Lightning-fast delivery across India
→ Trusted by thousands of happy customers

⚡ This exclusive offer won't last long!
👆 Shop now and get your FREE prescription lenses'''

ad_id, creative_id = create_perfect_ad(headline, primary_text, "Premium Eyewear + FREE Lenses")
```

---

## 🎯 AD FEATURES GUARANTEED

### ✅ What This Formula Delivers:
- **Ad Type**: Advantage+ catalogue ads
- **Format**: Carousel
- **Targeting**: Ray-Ban & Oakley interests (from existing ad set)
- **Budget**: Shares ₹2,500/day with ad set
- **Optimization**: Machine learning product selection
- **Images**: Automatic from GoEye Shopify catalog
- **Pricing**: Dynamic from catalog
- **Branding**: Frame overlay maintained

### 📊 Expected Performance:
- **CTR**: High (benefit-focused headlines)
- **Engagement**: Strong (emotional hooks + social proof)
- **Conversions**: Excellent (FREE prescription lenses value)
- **ROAS**: Optimized (premium positioning)

---

## ⚠️ CRITICAL RULES

### ✅ DO:
1. **Always create NEW ads** (never edit existing ones)
2. **Only change headline and primary text**
3. **Include FREE prescription lenses** in every ad
4. **Use the exact technical structure** provided
5. **Test different headlines/copy** with new ads
6. **Keep existing offers** (₹150 OFF + BOGO 50%)

### ❌ DON'T:
1. **Never edit existing ads** (display issues)
2. **Never change technical parameters**
3. **Never use product variables** in primary text
4. **Never remove FREE prescription lenses** offer
5. **Never change ad set, targeting, or budget**
6. **Never modify image layers or frame overlay**

---

## 🎨 CONTENT VARIATIONS

### Headlines (Rotate These):
1. "Premium Eyewear + FREE Prescription Lenses Inside!"
2. "FREE Prescription Lenses + Designer Frames!"
3. "Limited Time: FREE Lenses with Every Frame!"
4. "Transform Your Vision + Get FREE Prescription Lenses!"
5. "Designer Frames + FREE Prescription Lenses Deal!"

### Primary Text Hooks (Vary These):
- "🔥 EXCLUSIVE: Get FREE Prescription Lenses with Every Frame!"
- "🎯 FLASH SALE: FREE Prescription Lenses + Premium Frames!"
- "💎 PREMIUM DEAL: FREE Prescription Lenses Worth Thousands!"
- "⚡ LIMITED TIME: FREE Prescription Lenses + Designer Eyewear!"
- "🚀 BREAKTHROUGH OFFER: FREE Prescription Lenses Included!"

---

## 📈 SUCCESS METRICS

### Track These KPIs:
- **CTR**: Target >2%
- **CPC**: Monitor for efficiency
- **Conversion Rate**: Track purchases
- **ROAS**: Maintain >5.0
- **Engagement**: Comments, shares, reactions

### Optimization Strategy:
1. **Create 3-5 ad variations** with different headlines
2. **Let Facebook optimize** for 48-72 hours
3. **Pause low performers** (CTR <1.5%)
4. **Scale winners** by creating similar ads
5. **Always maintain** the technical structure

---

## 🎯 FINAL CHECKLIST

Before creating any ad, confirm:

- [ ] Using exact technical parameters
- [ ] Headline includes FREE prescription lenses
- [ ] Primary text has no product variables
- [ ] Existing offers (₹150 OFF + BOGO 50%) included
- [ ] Social proof and urgency present
- [ ] Clear call-to-action at end
- [ ] Creating NEW ad (not editing existing)
- [ ] Using same ad set for targeting consistency

---

## 💡 REMEMBER

**This formula is PERFECT.** 

- ✅ **Advantage+ catalog ads** with **carousel format**
- ✅ **Automatic product selection** from GoEye catalog  
- ✅ **Dynamic pricing** from Shopify
- ✅ **Expert targeting** (Ray-Ban & Oakley interests)
- ✅ **Premium positioning** of FREE prescription lenses
- ✅ **Proven conversion psychology**

**Only change headline and primary text. Everything else stays identical.**

---

*Last Updated: August 26, 2025*
*Status: PERFECT FORMULA - DO NOT MODIFY TECHNICAL STRUCTURE*
