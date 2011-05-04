from news.models import Submission, Comment
from django import forms

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        exclude = ('created_at', 'upvotes')


class CommentForm(forms.ModelForm):
    submission = forms.ModelChoiceField(
            queryset=Submission.objects.all(),
            widget = forms.HiddenInput(),
            required = False
            )

    
    parent= forms.ModelChoiceField(
            queryset=Comment.objects.all(),
            widget = forms.HiddenInput(),
            required = False
            )

    class Meta:
        model = Comment
        exclude = ('last_modified', 'submission', 'parent')
