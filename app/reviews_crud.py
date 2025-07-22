import sys
import os
from datetime import datetime, timezone

# Add parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import Review

app = create_app()

def list_reviews():
    """List all reviews"""
    with app.app_context():
        reviews = Review.query.all()
        if not reviews:
            print("\nNo reviews found.")
            return
        print("\nReview List:")
        print("=" * 50)
        for r in reviews:
            print(f"Review ID: {r.review_id}, User ID: {r.user_id}, Project ID: {r.project_id}, Rating: {r.rating}")
            print(f"Title: {r.title}")
            print("-" * 50)

def create_review():
    """Create a new review"""
    print("\nCreate New Review")
    print("=" * 50)

    try:
        with app.app_context():
            review = Review(
                project_id=int(input("Project ID: ").strip()),
                developer_id=int(input("Developer ID: ").strip()),
                user_id=int(input("User ID: ").strip()),
                rating=int(input("Overall Rating (1-5): ").strip()),
                title=input("Review Title: ").strip(),
                review_text=input("Review Text: ").strip(),
                pros=input("Pros: ").strip(),
                cons=input("Cons: ").strip(),
                construction_quality_rating=int(input("Construction Quality Rating (1-5): ").strip()),
                amenities_rating=int(input("Amenities Rating (1-5): ").strip()),
                location_rating=int(input("Location Rating (1-5): ").strip()),
                value_for_money_rating=int(input("Value for Money Rating (1-5): ").strip()),
                is_verified=bool(int(input("Is Verified (1/0): ").strip() or 0)),
                created_at=datetime.now(timezone.utc)
            )
            db.session.add(review)
            db.session.commit()
            print("\n✅ Review submitted successfully!")
    except Exception as e:
        print(f"\n❌ Error creating review: {str(e)}")

def read_review():
    """View a review by ID"""
    review_id = input("\nEnter Review ID to view: ").strip()
    with app.app_context():
        review = Review.query.get(review_id)
        if not review:
            print("\n❌ Review not found!")
            return
        print("\nReview Details:")
        print("=" * 50)
        for column in review.__table__.columns:
            print(f"{column.name}: {getattr(review, column.name)}")

def update_review():
    """Update a review"""
    review_id = input("\nEnter Review ID to update: ").strip()
    with app.app_context():
        review = Review.query.get(review_id)
        if not review:
            print("\n❌ Review not found!")
            return

        print("\nUpdate Review (leave blank to keep current value)")
        review.title = input(f"Title [{review.title}]: ") or review.title
        review.review_text = input(f"Review Text [{review.review_text[:30]}...]: ") or review.review_text
        review.rating = int(input(f"Overall Rating [{review.rating}]: ") or review.rating)
        review.is_verified = bool(int(input(f"Is Verified (1/0) [{int(review.is_verified)}]: ") or int(review.is_verified)))

        db.session.commit()
        print(f"\n✅ Review ID {review.review_id} updated successfully!")

def delete_review():
    """Delete a review"""
    review_id = input("\nEnter Review ID to delete: ").strip()
    with app.app_context():
        review = Review.query.get(review_id)
        if not review:
            print("\n❌ Review not found!")
            return

        confirm = input(f"Are you sure you want to delete review titled '{review.title}'? (yes/no): ").lower()
        if confirm == 'yes':
            db.session.delete(review)
            db.session.commit()
            print(f"\n✅ Review ID {review.review_id} deleted successfully!")
        else:
            print("\n❌ Deletion cancelled.")

def main_menu():
    while True:
        print("\nReview Management")
        print("=" * 30)
        print("1. List All Reviews")
        print("2. Create New Review")
        print("3. View Review Details")
        print("4. Update Review")
        print("5. Delete Review")
        print("0. Exit")

        choice = input("Enter your choice (0-5): ")

        if choice == '1':
            list_reviews()
        elif choice == '2':
            create_review()
        elif choice == '3':
            read_review()
        elif choice == '4':
            update_review()
        elif choice == '5':
            delete_review()
        elif choice == '0':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == '__main__':
    main_menu()
