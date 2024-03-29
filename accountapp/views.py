from random import shuffle
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import check_password
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator

from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy, reverse
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.views.generic import View, DeleteView, UpdateView, CreateView
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordResetView
from django.shortcuts import render, get_object_or_404, redirect

from django.contrib import messages

from django.conf import settings

from accountapp.decorators import account_ownership_required
from accountapp.forms import PasswordResetForm, CustomAuthenticationForm, UserForm, UserInfoForm
from accountapp.models import UserInfo
from excel_import.models import FoodModel
from accountapp.models import UserInfo


def homepage(request):
    VEGAN = list(FoodModel.objects.filter(VEGAN=1).all())
    HIGH_PRO = list(FoodModel.objects.filter(HIGH_PRO=1).all())
    LOW_NA = list(FoodModel.objects.filter(LOW_NA=1).all())
    DIETS = list(FoodModel.objects.filter(DIETS=1).all())
    #dislike_ingredient = request.GET.get('dislike_ingredient', '')
    #vegan_img,hp_img,ln_img,dt_img=dislike()
    # if dislike_ingredient:
    #     vegan_img = [recipe for recipe in vegan_img if dislike_ingredient not in recipe.RCP_PARTS_DTLS]
    #     hp_img = [recipe for recipe in hp_img if dislike_ingredient not in recipe.RCP_PARTS_DTLS]
    #     ln_img = [recipe for recipe in ln_img if dislike_ingredient not in recipe.RCP_PARTS_DTLS]
    #     dt_img = [recipe for recipe in dt_img if dislike_ingredient not in recipe.RCP_PARTS_DTLS]
    shuffle(VEGAN)
    shuffle(HIGH_PRO)
    shuffle(LOW_NA)
    shuffle(DIETS)
    if request.user.is_authenticated:
        user_id = request.user.id
        user_profile = get_object_or_404(UserInfo, user_id=user_id)
        return render(request, 'accountapp/home.html',{'vegan_img': VEGAN, 'hp_img': HIGH_PRO, 'ln_img': LOW_NA, 'dt_img': DIETS,'user_profile':user_profile})
    else:
        return render(request, 'accountapp/home.html')
# def dislike():
    # 싫어하는 재료를 입력받습니다.
    #dislike_ingredient = dislike_igt

    # 모든 레시피를 가져옵니다.


    # 사용자가 입력한 싫어하는 재료가 있을 경우 해당하는 레시피를 제거합니다.
    # if dislike_ingredient:
    #     vegan_img = [recipe for recipe in vegan_img if dislike_ingredient not in recipe.RCP_PARTS_DTLS]
    #     hp_img = [recipe for recipe in hp_img if dislike_ingredient not in recipe.RCP_PARTS_DTLS]
    #     ln_img = [recipe for recipe in ln_img if dislike_ingredient not in recipe.RCP_PARTS_DTLS]
    #     dt_img = [recipe for recipe in dt_img if dislike_ingredient not in recipe.RCP_PARTS_DTLS]
    # return (vegan_img,  hp_img,  ln_img, dt_img)
    # if dislike_ingredient:
    #     vegan_img = [recipe for recipe in vegan_img if dislike_ingredient not in recipe.RCP_PARTS_DTLS]
    #     hp_img = [recipe for recipe in hp_img if dislike_ingredient not in recipe.RCP_PARTS_DTLS]
    #     ln_img = [recipe for recipe in ln_img if dislike_ingredient not in recipe.RCP_PARTS_DTLS]
    #     dt_img = [recipe for recipe in dt_img if dislike_ingredient not in recipe.RCP_PARTS_DTLS]
    #
    # # 레시피 리스트를 섞습니다.
    # shuffle(vegan_img)
    # shuffle(hp_img)
    # shuffle(ln_img)
    # shuffle(dt_img)
    #
    # return (vegan_img,  hp_img,  ln_img, dt_img)

#회원가입
def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()        # 반환값 받아서 user에 저장
            auth_login(request, user) # 반환값 user를 인자로 auth_login() 해서 바로 로그인
            return redirect('accountapp:infocreate')
    else:
        form = UserForm()
    context = {
        'form': form,
    }
    return render(request, 'accountapp/signup.html', context)

#회원가입 시 개인정보 입력
class UserInfoCreateView(CreateView):
    model = UserInfo
    form_class = UserInfoForm
    context_object_name = 'target_userinfo'
    success_url = reverse_lazy('accountapp:home')
    template_name = 'accountapp/infocreate.html'
    def form_valid(self, form):
        info = form.save(commit=False)
        info.user = self.request.user
        info.save()
        return super().form_valid(form)

#개인정보 페이지에서 개인정보 수정 기능
@method_decorator(login_required, name='dispatch')
@method_decorator(account_ownership_required, name='dispatch')
class UserInfoUpdateView(UpdateView):
    model = UserInfo
    form_class = UserInfoForm
    context_object_name = 'target_userinfo'
    template_name = 'accountapp/infoupdate.html'

    def get_success_url(self):
        return reverse('mypageapp:mypage', kwargs={'pk': self.object.pk})

#로그인뷰
class CustomLoginView(auth_views.LoginView):
    form_class = CustomAuthenticationForm

#회원 탈퇴하기
@method_decorator(login_required, name='dispatch')
@method_decorator(account_ownership_required, name='dispatch')
class AccountDeleteView(DeleteView):
    model = User
    context_object_name = 'target_user'
    success_url = reverse_lazy('accountapp:home')
    template_name = 'accountapp/delete.html'

#마이페이지 내 비밀번호 변경 (기존 비밀번호 확인)
@method_decorator(login_required, name='dispatch')
@method_decorator(account_ownership_required, name='dispatch')
def change_pw(request,pk):
    context = {}
    if request.method == "POST":
        current_password = request.POST.get("origin_password")
        user = request.user
        if check_password(current_password, user.password):
            new_password = request.POST.get("password1")
            password_confirm = request.POST.get("password2")
            if new_password == password_confirm:
                user.set_password(new_password)
                user.save()
                return redirect("accountapp:home")

    return render(request,"accountapp/pw_update.html")

#아이디 찾기
def FindIDview(request):
    context = {}
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            if user is not None:
                template = render_to_string('email_template.html', {'nickname':user.userinfo.nickname, 'id':user.username})
                method_email = EmailMessage(
                    'Your ID is in the email', #메일 제목
                    template, #메일 내용 html
                    settings.EMAIL_HOST_USER, #메일 보내는 사람
                    [email],
                    )
                method_email.send(fail_silently=False) #메일 보내는 동안 오류 발생해도 무시하고 보냄
                return render(request, 'accountapp/id_sent.html', context) #메일 발송 시 성공 페이지로 연결
        except:
            messages.info(request, "해당 이메일로 가입한 아이디가 존재하지 않습니다.")
    context = {}
    return render(request, 'accountapp/id_find.html', context)

#비밀번호 찾기 (사용자ID, email 입력)
class PasswordResetView(auth_views.PasswordResetView):
    template_name = 'accountapp/password_reset.html'
    # success_url = reverse_lazy('password_reset_done')
    form_class = PasswordResetForm
    # email_template_name = 'common/password_reset_email.html'

#비밀번호 찾기 (메일 전송 완료)
class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'accountapp/password_reset_done.html'

#비밀번호 찾기 (새로운 비밀번호 입력)
class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'accountapp/password_reset_confirm.html'
    success_url = reverse_lazy('accountapp:login')

