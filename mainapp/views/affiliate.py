from django.shortcuts import render


def affiliateinfo(request):
    # Commission tiers: (upperLimit, rewardAmount)
    commissionTiers = [
        {"rangeMin": 0, "rangeMax": 2500, "reward": 100},
        {"rangeMin": 2500, "rangeMax": 3500, "reward": 150},
        {"rangeMin": 3500, "rangeMax": 5500, "reward": 200},
        {"rangeMin": 5500, "rangeMax": 6500, "reward": 300},
        {"rangeMin": 6500, "rangeMax": 7500, "reward": 350},
        {"rangeMin": 7500, "rangeMax": 9500, "reward": 450},
        {"rangeMin": 9500, "rangeMax": 10000, "reward": 500},
        {"rangeMin": 10000, "rangeMax": 12000, "reward": 1000}
    ]

    return render(request, 'AffiliateProgram/affiliateInfo.html', {
        "commissionTiers": commissionTiers
    })
