emails = [

    # 🟢 EASY (Spam)
    {
        "subject": "Congratulations! You won a lottery",
        "body": "Click this link to claim your prize now!!!",
        "label": "spam"
    },
    {
        "subject": "Limited Offer!!!",
        "body": "Buy now and get 90% discount on all products",
        "label": "spam"
    },

    # 🟡 MEDIUM (Customer Support)
    {
        "subject": "Damaged Product Received",
        "body": "I received a damaged item. Please help me with replacement.",
        "label": "normal"
    },
    {
        "subject": "Late Delivery Issue",
        "body": "My order is delayed and I am not happy. Please assist.",
        "label": "normal"
    },

    # 🔴 HARD (Urgent / Emotional tones)
    {
        "subject": "URGENT: Payment Failed",
        "body": "My payment was deducted but order not confirmed. Resolve immediately.",
        "label": "urgent"
    },
    {
        "subject": "Very Angry Customer",
        "body": "This is unacceptable! I want immediate resolution or I will complain publicly.",
        "label": "urgent"
    },
    {
        "subject": "Polite Request",
        "body": "Hi team, could you please help me with my issue? I would appreciate your support.",
        "label": "normal"
    }
]