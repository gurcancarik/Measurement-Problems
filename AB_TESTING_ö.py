#####################################################
# AB Testi ile BiddingYöntemlerinin Dönüşümünün Karşılaştırılması
#####################################################

#####################################################
# İş Problemi
#####################################################

# Facebook kısa süre önce mevcut "maximumbidding" adı verilen teklif verme türüne alternatif
# olarak yeni bir teklif türü olan "average bidding"’i tanıttı. Müşterilerimizden biri olan bombabomba.com,
# bu yeni özelliği test etmeye karar verdi veaveragebidding'in maximumbidding'den daha fazla dönüşüm
# getirip getirmediğini anlamak için bir A/B testi yapmak istiyor.A/B testi 1 aydır devam ediyor ve
# bombabomba.com şimdi sizden bu A/B testinin sonuçlarını analiz etmenizi bekliyor.Bombabomba.com için
# nihai başarı ölçütü Purchase'dır. Bu nedenle, istatistiksel testler için Purchasemetriğine odaklanılmalıdır.




#####################################################
# Veri Seti Hikayesi
#####################################################

# Bir firmanın web site bilgilerini içeren bu veri setinde kullanıcıların gördükleri ve tıkladıkları
# reklam sayıları gibi bilgilerin yanı sıra buradan gelen kazanç bilgileri yer almaktadır.Kontrol ve Test
# grubu olmak üzere iki ayrı veri seti vardır. Bu veri setleriab_testing.xlsxexcel’ininayrı sayfalarında yer
# almaktadır. Kontrol grubuna Maximum Bidding, test grubuna AverageBiddinguygulanmıştır.

# impression: Reklam görüntüleme sayısı
# Click: Görüntülenen reklama tıklama sayısı
# Purchase: Tıklanan reklamlar sonrası satın alınan ürün sayısı
# Earning: Satın alınan ürünler sonrası elde edilen kazanç



#####################################################
# Proje Görevleri
#####################################################

######################################################
# AB Testing (Bağımsız İki Örneklem T Testi)
######################################################

# 1. Hipotezleri Kur
# 2. Varsayım Kontrolü
#   - 1. Normallik Varsayımı (shapiro)
#   - 2. Varyans Homojenliği (levene)
# 3. Hipotezin Uygulanması
#   - 1. Varsayımlar sağlanıyorsa bağımsız iki örneklem t testi
#   - 2. Varsayımlar sağlanmıyorsa mannwhitneyu testi
# 4. p-value değerine göre sonuçları yorumla
# Not:
# - Normallik sağlanmıyorsa direkt 2 numara. Varyans homojenliği sağlanmıyorsa 1 numaraya arguman girilir.
# - Normallik incelemesi öncesi aykırı değer incelemesi ve düzeltmesi yapmak faydalı olabilir.


import itertools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
#!pip install statsmodels
import statsmodels.stats.api as sms
from scipy.stats import ttest_1samp, shapiro, levene, ttest_ind, mannwhitneyu, \
    pearsonr, spearmanr, kendalltau, f_oneway, kruskal
from statsmodels.stats.proportion import proportions_ztest

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 10)
pd.set_option('display.float_format', lambda x: '%.5f' % x)


#####################################################
# Görev 1:  Veriyi Hazırlama ve Analiz Etme
#####################################################

# Adım 1:  ab_testing_data.xlsx adlı kontrol ve test grubu verilerinden oluşan veri setini okutunuz. Kontrol ve test grubu verilerini ayrı değişkenlere atayınız.

df = pd.read_excel("C:/Users/ece/PycharmProjects/data_analysis_with_python.py/datasets/ab_testing.xlsx")

df_control = pd.read_excel("C:/Users/ece/PycharmProjects/data_analysis_with_python.py/datasets/ab_testing.xlsx", sheet_name="Control Group")
df_test = pd.read_excel("C:/Users/ece/PycharmProjects/data_analysis_with_python.py/datasets/ab_testing.xlsx", sheet_name="Test Group")


# Adım 2: Kontrol ve test grubu verilerini analiz ediniz.

control_group.describe()
test_group.describe()


# Adım 3: Analiz işleminden sonra concat metodunu kullanarak kontrol ve test grubu verilerini birleştiriniz.

import pandas as pd


# Grupları birleştir ve yeni bir sütun ekleyerek grup bilgisini belirt
control_group['group'] = 'Control'
test_group['group'] = 'Test'

grouped_data = pd.concat([control_group, test_group], axis=0)







#####################################################
# Görev 2:  A/B Testinin Hipotezinin Tanımlanması
#####################################################

# Adım 1: Hipotezi tanımlayınız.

 # H0: Kontrol grubu ve test grubu kazanç ortalamaları eşittir. (M1=M2)
 # H1: Kontrol grubu ve test grubu kazanç ortalamaları eşit değildir. (M1 != M2)

# Adım 2: Kontrol ve test grubu için purchase(kazanç) ortalamalarını analiz ediniz

control_mean = df_control["Purchase"].mean()
test_mean = df_test["Purchase"].mean()


#####################################################
# GÖREV 3: Hipotez Testinin Gerçekleştirilmesi
#####################################################



######################################################
# AB Testing (Bağımsız İki Örneklem T Testi)
######################################################


# Adım 1: Hipotez testi yapılmadan önce varsayım kontrollerini yapınız.Bunlar Normallik Varsayımı ve Varyans Homojenliğidir.

# Kontrol ve test grubunun normallik varsayımına uyup uymadığını Purchase değişkeni üzerinden ayrı ayrı test ediniz

test_stat, pvalue = shapiro(df_control.loc[:, "Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

test_stat, pvalue = shapiro(df_test.loc[:, "Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# Her iki grup için p değerleri
# Control grubu p değeri= 0.5891, Test grubu p değeri 0.15
# olarak bulunmuş ve p değerleri 0.05' ten büyük olduğundan dolayı normallik varsayımı
# sağlanmaktadır.


test_stat, pvalue = levene(df_control["Purchase"], df_test["Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# p değeri 0.1083 olarak hesaplanmıştır. 0.05' ten büyük olduğundan dolayı
# varyans homojenliği de sağlanmıştır.

# Adım 2: Normallik Varsayımı ve Varyans Homojenliği sonuçlarına göre uygun testi seçiniz

# normal dağılıma uygun , varyanslar homojen old için:
# bağımsız iki örneklem t testi uygulanmalıdır.

test_stat, pvalue = ttest_ind(grouped_data["Control_Purchase"],
                              grouped_data["Test_Purchase"],
                              equal_var=True)


# Adım 3: Test sonucunda elde edilen p_value değerini göz önünde bulundurarak kontrol ve test grubu satın alma
# ortalamaları arasında istatistiki olarak anlamlı bir fark olup olmadığını yorumlayınız.



t_stat, p_value = ttest_ind(df_control['Purchase'], df_test['Purchase'])

print(f"t-Testi İstatistik Değeri: {t_stat}, p-değeri: {p_value}")

# hesaplanan p değeri 0.3493 yani 0.05' ten büyük old için H0 kabul.
# İki grup arasında anlamlı bir fark yoktur

##############################################################
# GÖREV 4 : Sonuçların Analizi
##############################################################

# Adım 1: Hangi testi kullandınız, sebeplerini belirtiniz.

# 2 varsayım da sağlandığından dolayı bağımsız 2 örneklem t testi uygulamndı.


# Adım 2: Elde ettiğiniz test sonuçlarına göre müşteriye tavsiyede bulununuz.

