from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from web3 import Web3
import os

# Initialize Web3 connection using Alchemy Polygon mainnet RPC
ALCHEMY_URL = os.environ.get("ALCHEMY_POLYGON_RPC_URL", "https://polygon-mainnet.g.alchemy.com/v2/your_api_key")
w3 = Web3(Web3.HTTPProvider(ALCHEMY_URL))


def index(request):
    return render(request, 'index.html')


def _get_account_data(request):
    address = request.session.get('address')
    private_key = request.session.get('private_key')
    return address, private_key


def main(request):
    address, _ = _get_account_data(request)
    balance = 0
    if address and w3.isAddress(address):
        balance_wei = w3.eth.get_balance(address)
        balance = w3.fromWei(balance_wei, 'ether')
    return render(request, 'main.html', {'add': address, 'bal': balance, 'UncBal': 0})


def newTxn(request):
    address, private_key = _get_account_data(request)
    balance = 0
    if address and w3.isAddress(address):
        balance = w3.fromWei(w3.eth.get_balance(address), 'ether')

    if request.method == "POST" and address and private_key:
        dest_add = request.POST.get('add')
        amount = float(request.POST.get('amount'))
        acct = w3.eth.account.from_key(private_key)
        nonce = w3.eth.get_transaction_count(acct.address)
        tx = {
            'nonce': nonce,
            'to': dest_add,
            'value': w3.toWei(amount, 'ether'),
            'gas': 21000,
            'gasPrice': w3.eth.gas_price,
            'chainId': 137,
        }
        signed_tx = acct.sign_transaction(tx)
        w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        if request.user.is_authenticated:
            logout(request)
        return redirect('login')

    return render(request, 'newTxn.html', {'add': address, 'bal': balance, 'UncBal': 0})


def oldTxns(request):
    return render(request, 'oldTxns.html')


def profile(request):
    address, _ = _get_account_data(request)
    bal = 0
    if address and w3.isAddress(address):
        bal = w3.fromWei(w3.eth.get_balance(address), 'ether')
    return render(request, 'profile.html', {'add': address, 'bal': bal, 'UncBal': 0})


def wallet(request):
    address, _ = _get_account_data(request)
    bal = 0
    if address and w3.isAddress(address):
        bal = w3.fromWei(w3.eth.get_balance(address), 'ether')
    return render(request, 'wallet.html', {'add': address, 'bal': bal})


def register(request):
    if request.method == "POST":
        username = request.POST.get('name')
        email = request.POST.get('email')
        pas = request.POST.get('pas')
        user = User.objects.create_user(username=username, email=email, password=pas)
        user.save()
        acct = w3.eth.account.create()
        request.session['address'] = acct.address
        request.session['private_key'] = acct.privateKey.hex()
        return redirect("login")
    return render(request, "signup.html")


def loginpage(request):
    if request.method == "POST":
        name = request.POST.get('name')
        pwd = request.POST.get('pas')
        user = authenticate(request, username=name, password=pwd)
        if user is not None:
            login(request, user)
            return redirect("main")
        else:
            return redirect("login")
    return render(request, "login.html")


def logoutpage(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('login')


def address(request):
    address, _ = _get_account_data(request)
    return render(request, "address.html", {'address': address})


def qwertyuiop(request):
    return render(request, 'qwertyuiop.html')
