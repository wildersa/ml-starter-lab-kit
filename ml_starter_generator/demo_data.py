from __future__ import annotations

def get_demo_data(task: str, goal: str = "") -> str:
    """
    Returns deterministic synthetic CSV content for the given task and goal.
    Technical identifiers (column names) remain in English.
    """
    goal_lower = goal.lower()
    is_regression = any(keyword in goal_lower for keyword in ["number", "número", "2"])

    if task == "supervised":
        if is_regression:
            # P0.4: regression-style project (e.g., house price) with target 'price'
            return (
                "id,sqft,bedrooms,age,price\n"
                "1,1500,3,10,250000\n"
                "2,2000,4,5,350000\n"
                "3,1200,2,20,180000\n"
                "4,1800,3,15,280000\n"
                "5,2500,4,2,450000\n"
                "6,1600,3,12,260000\n"
                "7,2100,4,4,370000\n"
                "8,1100,2,25,170000\n"
                "9,1900,3,14,290000\n"
                "10,2600,4,1,470000\n"
            )
        else:
            # P0.3: classification-style project (e.g., bank campaign) with target 'subscribed'
            return (
                "id,age,job,balance,subscribed\n"
                "1,30,admin,2000,no\n"
                "2,45,technician,5000,yes\n"
                "3,25,services,500,no\n"
                "4,35,management,10000,yes\n"
                "5,50,retired,1500,no\n"
                "6,32,admin,2500,no\n"
                "7,42,technician,4800,yes\n"
                "8,28,services,600,no\n"
                "9,38,management,9500,yes\n"
                "10,55,retired,1200,no\n"
            )

    if task == "unsupervised":
        # P0.5: customer segmentation CSV with no target column
        return (
            "customer_id,age,annual_income,spend_score\n"
            "1,19,15000,39\n"
            "2,21,15000,81\n"
            "3,20,16000,6\n"
            "4,23,16000,77\n"
            "5,31,17000,40\n"
            "6,22,17000,76\n"
            "7,35,18000,6\n"
            "8,23,18000,94\n"
            "9,64,19000,3\n"
            "10,30,19000,72\n"
        )

    if task == "timeseries":
        # P0.6: daily sales CSV with date/value columns
        return (
            "date,sales,on_promotion\n"
            "2023-01-01,100,yes\n"
            "2023-01-02,120,yes\n"
            "2023-01-03,90,no\n"
            "2023-01-04,110,no\n"
            "2023-01-05,150,yes\n"
            "2023-01-06,140,yes\n"
            "2023-01-07,130,no\n"
            "2023-01-08,110,no\n"
            "2023-01-09,125,yes\n"
            "2023-01-10,160,yes\n"
        )

    if task == "vision":
        # P0.7: metadata CSV demo, no image binaries
        return (
            "image_path,label,width,height\n"
            "data/raw/images/img1.jpg,cat,640,480\n"
            "data/raw/images/img2.jpg,dog,640,480\n"
            "data/raw/images/img3.jpg,cat,640,480\n"
            "data/raw/images/img4.jpg,bird,640,480\n"
            "data/raw/images/img5.jpg,dog,640,480\n"
            "data/raw/images/img6.jpg,cat,640,480\n"
            "data/raw/images/img7.jpg,dog,640,480\n"
            "data/raw/images/img8.jpg,bird,640,480\n"
            "data/raw/images/img9.jpg,cat,640,480\n"
            "data/raw/images/img10.jpg,dog,640,480\n"
        )

    if task == "bandit":
        # Multi-Armed Bandit demo: arm name and reward
        return (
            "arm_name,reward\n"
            "arm_a,1\n"
            "arm_b,0\n"
            "arm_a,0\n"
            "arm_c,1\n"
            "arm_b,1\n"
            "arm_a,1\n"
            "arm_c,0\n"
            "arm_b,0\n"
            "arm_a,1\n"
            "arm_c,1\n"
        )

    # Default/Generic: minimal placeholder
    return (
        "feature1,feature2,target\n"
        "1.0,2.0,0\n"
        "2.0,1.0,1\n"
        "3.0,3.0,0\n"
        "4.0,2.5,1\n"
        "5.0,4.0,0\n"
    )
