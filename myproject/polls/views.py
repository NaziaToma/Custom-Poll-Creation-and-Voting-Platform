from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Poll, Choice, Profile
from django.db.models import F, Sum
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
from django.contrib.auth import get_backends
from django.conf import settings
from twilio.rest import Client
from .forms import ContactForm
from django.core.mail import send_mail
import matplotlib.pyplot as plt
import io
import os
from django.http import HttpResponse
from django.db.models import Count
from datetime import date
import matplotlib.font_manager as fm
import matplotlib
matplotlib.use('Agg') 



def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            # If phone_number was used earlier, remove or modify this section
            profile, created = Profile.objects.get_or_create(user=user)
            profile.date_of_birth = form.cleaned_data.get('date_of_birth')
            profile.country = form.cleaned_data.get('country')
            profile.district = form.cleaned_data.get('district')
            profile.save()

            return redirect('polls:index')  # Modify as per your needs
        else:
            form.add_error(None, "There was an error with your signup.")
    else:
        form = CustomUserCreationForm()  # Ensure this is initialized for GET requests

    return render(request, 'polls/signup.html', {'form': form})

def index(request):
    latest_poll_list = Poll.objects.order_by('-pub_date')[:5]

    polls_with_results = []
    for poll in latest_poll_list:
        total_votes = poll.choice_set.aggregate(Sum('votes'))['votes__sum'] or 0
        choices = poll.choice_set.all()
        polls_with_results.append({
            'poll': poll,
            'total_votes': total_votes,
            'choices': choices,
        })

    context = {'polls_with_results': polls_with_results}
    return render(request, 'polls/index.html', context)

@login_required
def detail(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    total_votes = poll.choice_set.aggregate(Sum('votes'))['votes__sum'] or 0
    return render(request, 'polls/detail.html', {'poll': poll, 'total_votes': total_votes})

@login_required
def vote(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    try:
        selected_choice = poll.choice_set.get(pk=request.POST['choice'])
        previous_vote = request.session.get(f'poll_{poll_id}_vote')
        
        if previous_vote and previous_vote != selected_choice.id:
            previous_choice = poll.choice_set.get(pk=previous_vote)
            previous_choice.votes = F('votes') - 1
            previous_choice.save()

        # Associate the vote with the current user
        selected_choice.votes = F('votes') + 1
        selected_choice.user = request.user  # Track the user who voted
        selected_choice.save()
        
        request.session[f'poll_{poll_id}_vote'] = selected_choice.id
    except (KeyError, Choice.DoesNotExist):
        total_votes = poll.choice_set.aggregate(Sum('votes'))['votes__sum'] or 0
        return render(request, 'polls/detail.html', {
            'poll': poll,
            'error_message': "You didn't select a choice.",
            'total_votes': total_votes,
        })
    return redirect('polls:detail', poll_id=poll.id)

@login_required
def results(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    total_votes = poll.choice_set.filter(user__isnull=False).aggregate(Sum('votes'))['votes__sum'] or 0
    return render(request, 'polls/results.html', {'poll': poll, 'total_votes': total_votes})

@login_required
def clear_vote(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    previous_vote = request.session.get(f'poll_{poll_id}_vote')
    if previous_vote:
        previous_choice = poll.choice_set.get(pk=previous_vote)
        previous_choice.votes = F('votes') - 1
        previous_choice.save()
        del request.session[f'poll_{poll_id}_vote']
    return redirect('polls:detail', poll_id=poll.id)

def about_us(request):
    return render(request, 'polls/about_us.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            sender = form.cleaned_data['email']

            recipients = [settings.DEFAULT_FROM_EMAIL]  # Use the email you set in your settings

            send_mail(subject, message, sender, recipients)

            return render(request, 'polls/contact_success.html')  # A page to show on successful submission
    else:
        form = ContactForm()

    return render(request, 'polls/contact.html', {'form': form})

def calculate_age(born):
    today = date.today()
    try:
        birthday = born.replace(year=today.year)
    except ValueError:  # Raised when birth date is February 29 and the current year is not a leap year
        birthday = born.replace(year=today.year, month=born.month + 1, day=1)
    if birthday > today:
        return today.year - born.year - 1
    else:
        return today.year - born.year

def age_chart(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    choices = poll.choice_set.all()

    age_ranges = {
        'Under 18': [0] * len(choices),
        '18-25': [0] * len(choices),
        '26-35': [0] * len(choices),
        '36-45': [0] * len(choices),
        '46-60': [0] * len(choices),
        '60+': [0] * len(choices),
        'Unknown': [0] * len(choices),
    }

    for choice_index, choice in enumerate(choices):
        if choice.user:
            profile = Profile.objects.get(user=choice.user)
            dob = profile.date_of_birth
            if dob is None:
                age_ranges['Unknown'][choice_index] += 1
            else:
                age = (date.today().year - dob.year)
                if age < 18:
                    age_ranges['Under 18'][choice_index] += 1
                elif 18 <= age <= 25:
                    age_ranges['18-25'][choice_index] += 1
                elif 26 <= age <= 35:
                    age_ranges['26-35'][choice_index] += 1
                elif 36 <= age <= 45:
                    age_ranges['36-45'][choice_index] += 1
                elif 46 <= age <= 60:
                    age_ranges['46-60'][choice_index] += 1
                else:
                    age_ranges['60+'][choice_index] += 1

    # Use a default font that supports both English and Bangla
    plt.rcParams['font.family'] = 'Arial'  # Replace 'Arial' with a font that supports both languages

    # If you are using a specific Bangla font, set it explicitly
    bangla_font_path = os.path.join(settings.BASE_DIR, 'fonts', 'SolaimanLipi.ttf')
    bangla_prop = fm.FontProperties(fname=bangla_font_path)

    fig, ax = plt.subplots(figsize=(10, 7))
    bar_width = 0.1
    index = range(len(choices))

    for i, (age_range, values) in enumerate(age_ranges.items()):
        ax.bar(
            [x + i * bar_width for x in index],
            values,
            bar_width,
            label=f'{age_range}',
            align='center'
        )

    ax.set_xlabel('Choices', fontproperties=None)  # Default font for English
    ax.set_ylabel('Number of Votes', fontproperties=None)  # Default font for English
    ax.set_title('Votes by Age Range and Choice', fontproperties=None)  # Default font for English
    ax.set_xticks([x + bar_width * (len(age_ranges) / 2) for x in index])
    ax.set_xticklabels([choice.choice_text for choice in choices], fontproperties=bangla_prop)  # Bangla font for choices if in Bangla
    ax.legend(title='Age Range')

    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)

    return HttpResponse(buf, content_type='image/png')