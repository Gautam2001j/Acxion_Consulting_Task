from django import forms
from .models import Book, Transaction, Membership

class BookIssueForm(forms.Form):
    book_id = forms.IntegerField()
    user_id = forms.IntegerField()
    issue_date = forms.DateField()
    return_date = forms.DateField()

class MembershipForm(forms.ModelForm):
    class Meta:
        model = Membership
        fields = ['first_name', 'last_name', 'contact_name', 'contact_address',
                  'aadhar_card_number', 'start_date', 'end_date', 'membership_duration']
