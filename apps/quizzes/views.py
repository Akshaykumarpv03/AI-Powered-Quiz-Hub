# apps/quizzes/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.core.models import Topic
from apps.quizzes.services import generate_question
from apps.quizzes.models import QuestionBank


@login_required
def create_quiz(request):
    topics = Topic.objects.select_related('subcategory__category').all()

    if request.method == "POST":
        try:
            topic_id = int(request.POST["topic"])
            difficulty = request.POST["difficulty"].lower()
            count = int(request.POST["count"])

            if count < 1 or count > 50:
                messages.error(request, "Please choose 1–50 questions.")
                return redirect('create_quiz')

            topic = Topic.objects.get(id=topic_id)
            generated_questions = []

            # Show a nice loading message
            messages.info(request, f"Generating {count} AI questions on '{topic.name}'... Please wait")

            for i in range(count):
                q = generate_question(topic_id=topic_id, difficulty=difficulty)
                if q:
                    generated_questions.append(q)
                else:
                    messages.warning(request, f"Question {i+1} failed to generate — skipped.")

            if not generated_questions:
                messages.error(request, "No questions were generated. Try again.")
                return redirect('create_quiz')

            return render(request, "quizzes/preview.html", {
                "questions": generated_questions,
                "quiz_title": f"{topic.name} - {difficulty.title()} ({count} Qs)"
            })

        except Exception as e:
            messages.error(request, "Something went wrong. Please try again.")
            print("Quiz generation error:", e)

    return render(request, "quizzes/create.html", {"topics": topics})