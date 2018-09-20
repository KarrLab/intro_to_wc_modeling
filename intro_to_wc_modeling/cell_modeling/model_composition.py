""" Model composition tutorial

- Glycolysis model (Teusink et al., 2000)
- Glycerol synthesis model (Cronwright et al., 2002)

:Author: Jonathan Karr <jonrkarr@gmail.com>
:Author: Yin Hoon Chew <yinhoon.chew@mssm.edu>
:Date: 2017-08-30
:Copyright: 2017, Karr Lab
:License: MIT
"""

from scipy.integrate import odeint
from matplotlib import pyplot
import matplotlib
import numpy
import os


class GlycolysisModel(object):
    """ Glycolysis model (Teusink et al., 2000)

    Based on the `version from JWS Online <http://jjj.biochem.sun.ac.za/models/teusink/>`_

    Attributes:
        CPFKAMP (obj:`float`):
        CPFKATP (obj:`float`):
        CPFKF16BP (obj:`float`):
        CPFKF26BP (obj:`float`):
        CPFKF6P (obj:`float`):
        CiPFKATP (obj:`float`):
        F26BP (obj:`float`):
        KATPASE (obj:`float`):
        KGLYCOGEN (obj:`float`):
        KPFKAMP (obj:`float`):
        KPFKF16BP (obj:`float`):
        KPFKF26BP (obj:`float`):
        KSUCC (obj:`float`):
        KTREHALOSE (obj:`float`):
        KeqADH (obj:`float`):
        KeqAK (obj:`float`):
        KeqALD (obj:`float`):
        KeqENO (obj:`float`):
        KeqG3PDH (obj:`float`):
        KeqGLK (obj:`float`):
        KeqGLT (obj:`float`):
        KeqPGI (obj:`float`):
        KeqPGK (obj:`float`):
        KeqPGM (obj:`float`):
        KeqPYK (obj:`float`):
        KeqTPI (obj:`float`): ratio of GAP to DHAP at equilibrium
        KiADHACE (obj:`float`):
        KiADHETOH (obj:`float`):
        KiADHNAD (obj:`float`):
        KiADHNADH (obj:`float`):
        KiPFKATP (obj:`float`):
        KmADHACE (obj:`float`):
        KmADHETOH (obj:`float`):
        KmADHNAD (obj:`float`):
        KmADHNADH (obj:`float`):
        KmALDDHAP (obj:`float`):
        KmALDF16P (obj:`float`):
        KmALDGAP (obj:`float`):
        KmALDGAPi (obj:`float`):
        KmENOP2G (obj:`float`):
        KmENOPEP (obj:`float`):
        KmG3PDHDHAP (obj:`float`):
        KmG3PDHGLY (obj:`float`):
        KmG3PDHNAD (obj:`float`):
        KmG3PDHNADH (obj:`float`):
        KmGAPDHBPG (obj:`float`):
        KmGAPDHGAP (obj:`float`):
        KmGAPDHNAD (obj:`float`):
        KmGAPDHNADH (obj:`float`):
        KmGLKADP (obj:`float`):
        KmGLKATP (obj:`float`):
        KmGLKG6P (obj:`float`):
        KmGLKGLCi (obj:`float`):
        KmGLTGLCi (obj:`float`):
        KmGLTGLCo (obj:`float`):
        KmPDCPYR (obj:`float`):
        KmPFKATP (obj:`float`):
        KmPFKF6P (obj:`float`):
        KmPGIF6P (obj:`float`):
        KmPGIG6P (obj:`float`):
        KmPGKADP (obj:`float`):
        KmPGKATP (obj:`float`):
        KmPGKBPG (obj:`float`):
        KmPGKP3G (obj:`float`):
        KmPGMP2G (obj:`float`):
        KmPGMP3G (obj:`float`):
        KmPYKADP (obj:`float`):
        KmPYKATP (obj:`float`):
        KmPYKPEP (obj:`float`):
        KmPYKPYR (obj:`float`):
        L0 (obj:`float`):
        SUMAXP (obj:`float`):
        VmADH (obj:`float`):
        VmALD (obj:`float`):
        VmENO (obj:`float`):
        VmG3PDH (obj:`float`):
        VmGAPDHf (obj:`float`):
        VmGAPDHr (obj:`float`):
        VmGLK (obj:`float`):
        VmGLT (obj:`float`):
        VmPDC (obj:`float`):
        VmPFK (obj:`float`):
        VmPGI (obj:`float`):
        VmPGK (obj:`float`):
        VmPGM (obj:`float`):
        VmPYK (obj:`float`):
        gR (obj:`float`):
        nPDC (obj:`float`):
        CO2 (obj:`float`):
        ETOH (obj:`float`):
        GLCo (obj:`float`):
        GLY (obj:`float`):
        SUCC (obj:`float`):
        Trh (obj:`float`):

        ACE_0 (:obj:`float`): initial ACE concentration (mM)
        BPG_0 (:obj:`float`): initial BPG concentration (mM)
        F16BP_0 (:obj:`float`): initial F16BP concentration (mM)
        F6P_0 (:obj:`float`): initial F6P concentration (mM)
        G6P_0 (:obj:`float`): initial G6P concentration (mM)
        GLCi_0 (:obj:`float`): initial GLCi concentration (mM)
        NAD_0 (:obj:`float`): initial NAD concentration (mM)
        NADH_0 (:obj:`float`): initial NADH concentration (mM)
        P2G_0 (:obj:`float`): initial P2G concentration (mM)
        P3G_0 (:obj:`float`): initial P3G concentration (mM)
        PEP_0 (:obj:`float`): initial PEP concentration (mM)
        PYR_0 (:obj:`float`): initial PYR concentration (mM)
        Prb_0 (:obj:`float`): initial high energy phosphates (2*ATP + ADP) concentration (mM)
        TRIO_0 (:obj:`float`): initial triose-phosphate (DHAP + GAP) concentration (mM)

        x_0 (:obj:`numpy.array`): initial species concentrations (mM)
    """

    CPFKAMP = 0.0845
    CPFKATP = 3.0
    CPFKF16BP = 0.397
    CPFKF26BP = 0.0174
    CPFKF6P = 0.0
    CiPFKATP = 100.0
    F26BP = 0.02
    KATPASE = 39.5
    KGLYCOGEN = 6.0
    KPFKAMP = 0.0995
    KPFKF16BP = 0.111
    KPFKF26BP = 0.000682
    KSUCC = 21.4
    KTREHALOSE = 2.4
    KeqADH = 6.9e-05
    KeqAK = 0.45
    KeqALD = 0.069
    KeqENO = 6.7
    KeqG3PDH = 4300.0
    KeqGLK = 3800.0
    KeqGLT = 1.0
    KeqPGI = 0.314
    KeqPGK = 3200.0
    KeqPGM = 0.19
    KeqPYK = 6500.0
    KeqTPI = 0.045
    KiADHACE = 1.1
    KiADHETOH = 90.0
    KiADHNAD = 0.92
    KiADHNADH = 0.031
    KiPFKATP = 0.65
    KmADHACE = 1.11
    KmADHETOH = 17.0
    KmADHNAD = 0.17
    KmADHNADH = 0.11
    KmALDDHAP = 2.4
    KmALDF16P = 0.3
    KmALDGAP = 2.0
    KmALDGAPi = 10.0
    KmENOP2G = 0.04
    KmENOPEP = 0.5
    KmG3PDHDHAP = 0.4
    KmG3PDHGLY = 1.0
    KmG3PDHNAD = 0.93
    KmG3PDHNADH = 0.023
    KmGAPDHBPG = 0.0098
    KmGAPDHGAP = 0.21
    KmGAPDHNAD = 0.09
    KmGAPDHNADH = 0.06
    KmGLKADP = 0.23
    KmGLKATP = 0.15
    KmGLKG6P = 30.0
    KmGLKGLCi = 0.08
    KmGLTGLCi = 1.1918
    KmGLTGLCo = 1.1918
    KmPDCPYR = 4.33
    KmPFKATP = 0.71
    KmPFKF6P = 0.1
    KmPGIF6P = 0.3
    KmPGIG6P = 1.4
    KmPGKADP = 0.2
    KmPGKATP = 0.3
    KmPGKBPG = 0.003
    KmPGKP3G = 0.53
    KmPGMP2G = 0.08
    KmPGMP3G = 1.2
    KmPYKADP = 0.53
    KmPYKATP = 1.5
    KmPYKPEP = 0.14
    KmPYKPYR = 21.0
    L0 = 0.66
    SUMAXP = 4.1
    VmADH = 810.0
    VmALD = 322.258
    VmENO = 365.806
    VmG3PDH = 70.15
    VmGAPDHf = 1184.52
    VmGAPDHr = 6549.68
    VmGLK = 226.452
    VmGLT = 97.264
    VmPDC = 174.194
    VmPFK = 182.903
    VmPGI = 339.677
    VmPGK = 1306.45
    VmPGM = 2525.81
    VmPYK = 1088.71
    gR = 1.12
    nPDC = 1.9
    CO2 = 1.0
    ETOH = 50.0
    GLCo = 50.0
    GLY = 0.15
    SUCC = 0.0
    Trh = 0.0

    ACE_0 = 0.04
    BPG_0 = 0.0
    F16BP_0 = 0.1
    F6P_0 = 0.28
    G6P_0 = 1.39
    GLCi_0 = 0.087
    NAD_0 = 1.2
    NADH_0 = 0.39
    P2G_0 = 0.1
    P3G_0 = 0.1
    PEP_0 = 0.1
    PYR_0 = 3.36
    Prb_0 = 5.0
    TRIO_0 = 5.17

    @property
    def x_0(self):
        return numpy.array([
            self.ACE_0,
            self.BPG_0,
            self.F16BP_0,
            self.F6P_0,
            self.G6P_0,
            self.GLCi_0,
            self.NAD_0,
            self.NADH_0,
            self.P2G_0,
            self.P3G_0,
            self.PEP_0,
            self.PYR_0,
            self.Prb_0,
            self.TRIO_0,
        ])

    def v_1(self, x):
        # Hexokinase
        # GLCi + Prb <=> G6P
        return (self.VmGLK*(-((x[4]*(self.SUMAXP - (self.SUMAXP**2 - 2*self.SUMAXP*x[12] + 8*self.KeqAK*self.SUMAXP*x[12] + x[12]**2 - 4*self.KeqAK*x[12]**2)**0.5)) /
                              ((1 - 4*self.KeqAK)*self.KeqGLK)) + (x[5]*(-self.SUMAXP + x[12] - 4*self.KeqAK*x[12] + (self.SUMAXP**2 - 2*self.SUMAXP*x[12] + 8*self.KeqAK*self.SUMAXP*x[12] + x[12]**2 - 4*self.KeqAK*x[12]**2)**0.5))/(2 - 8*self.KeqAK)))/(self.KmGLKATP*self.KmGLKGLCi*(1 + x[4]/self.KmGLKG6P + x[5]/self.KmGLKGLCi)*(1 + (self.SUMAXP - (self.SUMAXP**2 - 2*self.SUMAXP*x[12] + 8*self.KeqAK*self.SUMAXP*x[12] + x[12]**2 - 4*self.KeqAK*x[12]**2)**0.5)/((1 - 4*self.KeqAK)*self.KmGLKADP) + (-self.SUMAXP + x[12] - 4*self.KeqAK*x[12] + (self.SUMAXP**2 - 2*self.SUMAXP*x[12] + 8*self.KeqAK*self.SUMAXP*x[12] + x[12]**2 - 4*self.KeqAK*x[12]**2)**0.5)/((2 - 8*self.KeqAK)*self.KmGLKATP)))

    def v_2(self, x):
        # Glucose-6-phosphate isomerase
        # G6P <=> F6P
        return (self.VmPGI*(-(x[3]/self.KeqPGI) + x[4]))/(self.KmPGIG6P*(1 + x[3]/self.KmPGIF6P + x[4]/self.KmPGIG6P))

    def v_3(self, x):
        # Glycogen synthesis
        # G6P + Prb => Glyc
        return self.KGLYCOGEN

    def v_4(self, x):
        # Trehalose 6-phosphate synthase
        # {2.0}G6P + Prb => Trh
        return self.KTREHALOSE

    def v_5(self, x):
        # Phosphofructokinase
        # F6P + Prb => F16P
        return (self.gR*self.VmPFK*x[3]*(-self.SUMAXP + x[12] - 4*self.KeqAK*x[12] + (self.SUMAXP**2 - 2*self.SUMAXP*x[12] + 8*self.KeqAK*self.SUMAXP*x[12] + x[12]**2 - 4*self.KeqAK*x[12]**2)**0.5)*(1 + x[3]/self.KmPFKF6P + (-self.SUMAXP + x[12] - 4*self.KeqAK*x[12] + (self.SUMAXP**2 - 2*self.SUMAXP*x[12] + 8*self.KeqAK*self.SUMAXP*x[12] + x[12]**2 - 4*self.KeqAK*x[12]**2)**0.5)/((2 - 8*self.KeqAK)*self.KmPFKATP) + (self.gR*x[3]*(-self.SUMAXP + x[12] - 4*self.KeqAK*x[12] + (self.SUMAXP**2 - 2*self.SUMAXP*x[12] + 8*self.KeqAK*self.SUMAXP*x[12] + x[12]**2 - 4*self.KeqAK*x[12]**2)**0.5))/((2 - 8*self.KeqAK)*self.KmPFKATP*self.KmPFKF6P)))/((2 - 8*self.KeqAK)*self.KmPFKATP*self.KmPFKF6P*((self.L0*(1 + (self.CPFKF26BP*self.F26BP)/self.KPFKF26BP + (self.CPFKF16BP*x[2])/self.KPFKF16BP)**2*(1 + (2*self.CPFKAMP*self.KeqAK*(self.SUMAXP - (self.SUMAXP**2 - 2*self.SUMAXP*x[12] + 8*self.KeqAK*self.SUMAXP*x[12] + x[12]**2 - 4*self.KeqAK*x[12]**2)**0.5)**2)/((-1 + 4*self.KeqAK)*self.KPFKAMP*(self.SUMAXP - x[12] + 4*self.KeqAK*x[12] - (self.SUMAXP**2 - 2*self.SUMAXP*x[12] + 8*self.KeqAK*self.SUMAXP*x[12] + x[12]**2 - 4*self.KeqAK*x[12]**2)**0.5)))**2*(1 + (self.CiPFKATP*(-self.SUMAXP + x[12] - 4*self.KeqAK*x[12] + (self.SUMAXP**2 - 2*self.SUMAXP*x[12] + 8*self.KeqAK*self.SUMAXP*x[12] + x[12]**2 - 4*self.KeqAK*x[12]**2)**0.5))/((2 - 8*self.KeqAK)*self.KiPFKATP))**2*(1 + (self.CPFKATP*(-self.SUMAXP + x[12] - 4*self.KeqAK*x[12] + (self.SUMAXP**2 - 2*self.SUMAXP*x[12] + 8*self.KeqAK*self.SUMAXP*x[12] + x[12]**2 - 4*self.KeqAK*x[12]**2)**0.5))/((2 - 8*self.KeqAK)*self.KmPFKATP))**2)/((1 + self.F26BP/self.KPFKF26BP + x[2]/self.KPFKF16BP)**2*(1 + (2*self.KeqAK*(self.SUMAXP - (self.SUMAXP**2 - 2*self.SUMAXP*x[12] + 8*self.KeqAK*self.SUMAXP*x[12] + x[12]**2 - 4*self.KeqAK*x[12]**2)**0.5)**2)/((-1 + 4*self.KeqAK)*self.KPFKAMP*(self.SUMAXP - x[12] + 4*self.KeqAK*x[12] - (self.SUMAXP**2 - 2*self.SUMAXP*x[12] + 8*self.KeqAK*self.SUMAXP*x[12] + x[12]**2 - 4*self.KeqAK*x[12]**2)**0.5)))**2*(1 + (-self.SUMAXP + x[12] - 4*self.KeqAK*x[12] + (self.SUMAXP**2 - 2*self.SUMAXP*x[12] + 8*self.KeqAK*self.SUMAXP*x[12] + x[12]**2 - 4*self.KeqAK*x[12]**2)**0.5)/((2 - 8*self.KeqAK)*self.KiPFKATP))**2) + (1 + x[3]/self.KmPFKF6P + (-self.SUMAXP + x[12] - 4*self.KeqAK*x[12] + (self.SUMAXP**2 - 2*self.SUMAXP*x[12] + 8*self.KeqAK*self.SUMAXP*x[12] + x[12]**2 - 4*self.KeqAK*x[12]**2)**0.5)/((2 - 8*self.KeqAK)*self.KmPFKATP) + (self.gR*x[3]*(-self.SUMAXP + x[12] - 4*self.KeqAK*x[12] + (self.SUMAXP**2 - 2*self.SUMAXP*x[12] + 8*self.KeqAK*self.SUMAXP*x[12] + x[12]**2 - 4*self.KeqAK*x[12]**2)**0.5))/((2 - 8*self.KeqAK)*self.KmPFKATP*self.KmPFKF6P))**2))

    def v_6(self, x):
        # Aldolase
        # F16P <=> {2.0}TRIO
        return (self.VmALD*(x[2] - (self.KeqTPI*x[13]**2)/(self.KeqALD*(1 + self.KeqTPI)**2)))/(self.KmALDF16P*(1 + x[2]/self.KmALDF16P + x[13]/((1 + self.KeqTPI)*self.KmALDDHAP) + (self.KeqTPI*x[13])/((1 + self.KeqTPI)*self.KmALDGAP) + (self.KeqTPI*x[2]*x[13])/((1 + self.KeqTPI)*self.KmALDF16P*self.KmALDGAPi) + (self.KeqTPI*x[13]**2)/((1 + self.KeqTPI)**2*self.KmALDDHAP*self.KmALDGAP)))

    def v_7(self, x):
        # Glyceraldehyde 3-phosphate dehydrogenase
        # TRIO + NAD <=> BPG + NADH
        return (-((self.VmGAPDHr*x[1]*x[7])/(self.KmGAPDHBPG*self.KmGAPDHNADH)) + (self.KeqTPI*self.VmGAPDHf*x[6]*x[13])/((1 + self.KeqTPI)*self.KmGAPDHGAP*self.KmGAPDHNAD))/((1 + x[6]/self.KmGAPDHNAD + x[7]/self.KmGAPDHNADH)*(1 + x[1]/self.KmGAPDHBPG + (self.KeqTPI*x[13])/((1 + self.KeqTPI)*self.KmGAPDHGAP)))

    def v_8(self, x):
        # Phosphoglycerate kinase
        # BPG <=> P3G + Prb
        return (self.VmPGK*((self.KeqPGK*x[1]*(self.SUMAXP - (self.SUMAXP**2 - 2*self.SUMAXP*x[12] + 8*self.KeqAK*self.SUMAXP*x[12] + x[12]**2 - 4*self.KeqAK*x[12]**2)**0.5))/(1 - 4*self.KeqAK) - (x[9]*(-self.SUMAXP + x[12] - 4*self.KeqAK*x[12] + (self.SUMAXP**2 - 2*self.SUMAXP*x[12] + 8*self.KeqAK*self.SUMAXP*x[12] + x[12]**2 - 4*self.KeqAK*x[12]**2)**0.5))/(2 - 8*self.KeqAK)))/(self.KmPGKATP*self.KmPGKP3G*(1 + x[1]/self.KmPGKBPG + x[9]/self.KmPGKP3G)*(1 + (self.SUMAXP - (self.SUMAXP**2 - 2*self.SUMAXP*x[12] + 8*self.KeqAK*self.SUMAXP*x[12] + x[12]**2 - 4*self.KeqAK*x[12]**2)**0.5)/((1 - 4*self.KeqAK)*self.KmPGKADP) + (-self.SUMAXP + x[12] - 4*self.KeqAK*x[12] + (self.SUMAXP**2 - 2*self.SUMAXP*x[12] + 8*self.KeqAK*self.SUMAXP*x[12] + x[12]**2 - 4*self.KeqAK*x[12]**2)**0.5)/((2 - 8*self.KeqAK)*self.KmPGKATP)))

    def v_9(self, x):
        # Phosphoglycerate mutase
        # P3G <=> P2G
        return (self.VmPGM*(-(x[8]/self.KeqPGM) + x[9]))/(self.KmPGMP3G*(1 + x[8]/self.KmPGMP2G + x[9]/self.KmPGMP3G))

    def v_10(self, x):
        # Enolase
        # P2G <=> PEP
        return (self.VmENO*(x[8] - x[10]/self.KeqENO))/(self.KmENOP2G*(1 + x[8]/self.KmENOP2G + x[10]/self.KmENOPEP))

    def v_11(self, x):
        # Pyruvate kinase
        # PEP <=> PYR + Prb
        return (self.VmPYK*((x[10]*(self.SUMAXP - (self.SUMAXP**2 - 2*self.SUMAXP*x[12] + 8*self.KeqAK*self.SUMAXP*x[12] + x[12]**2 - 4*self.KeqAK*x[12]**2)**0.5))/(1 - 4*self.KeqAK) - ((-self.SUMAXP + x[12] - 4*self.KeqAK*x[12] + (self.SUMAXP**2 - 2*self.SUMAXP*x[12] + 8*self.KeqAK*self.SUMAXP*x[12] + x[12]**2 - 4*self.KeqAK*x[12]**2)**0.5)*x[11])/((2 - 8*self.KeqAK)*self.KeqPYK)))/(self.KmPYKADP*self.KmPYKPEP*(1 + (self.SUMAXP - (self.SUMAXP**2 - 2*self.SUMAXP*x[12] + 8*self.KeqAK*self.SUMAXP*x[12] + x[12]**2 - 4*self.KeqAK*x[12]**2)**0.5)/((1 - 4*self.KeqAK)*self.KmPYKADP) + (-self.SUMAXP + x[12] - 4*self.KeqAK*x[12] + (self.SUMAXP**2 - 2*self.SUMAXP*x[12] + 8*self.KeqAK*self.SUMAXP*x[12] + x[12]**2 - 4*self.KeqAK*x[12]**2)**0.5)/((2 - 8*self.KeqAK)*self.KmPYKATP))*(1 + x[10]/self.KmPYKPEP + x[11]/self.KmPYKPYR))

    def v_12(self, x):
        # Pyruvate decarboxylase
        # PYR => CO2 + ACE
        return (self.VmPDC*x[11]**self.nPDC)/(self.KmPDCPYR**self.nPDC*(1 + x[11]**self.nPDC/self.KmPDCPYR**self.nPDC))

    def v_13(self, x):
        # Succinate synthesis
        # {2.0}ACE + {3.0}NAD => SUCC + {3.0}NADH
        return self.KSUCC*x[0]

    def v_14(self, x):
        # Glucose transport
        # GLCo <=> GLCi
        return (self.VmGLT*(self.GLCo - x[5]/self.KeqGLT))/(self.KmGLTGLCo*(1 + self.GLCo/self.KmGLTGLCo + x[5]/self.KmGLTGLCi + (0.91*self.GLCo*x[5])/(self.KmGLTGLCi*self.KmGLTGLCo)))

    def v_15(self, x):
        # Alcohol dehydrogenase
        # ACE + NADH <=> NAD + ETOH
        return -((self.VmADH*(self.ETOH*x[6] - (x[0]*x[7])/self.KeqADH))/(self.KiADHNAD*self.KmADHETOH*(1 + (self.ETOH*self.KmADHNAD)/(self.KiADHNAD*self.KmADHETOH) + (self.KmADHNADH*x[0])/(self.KiADHNADH*self.KmADHACE) + x[6]/self.KiADHNAD + (self.ETOH*x[6])/(self.KiADHNAD*self.KmADHETOH) + (self.ETOH*x[0]*x[6])/(self.KiADHACE*self.KiADHNAD*self.KmADHETOH) + (self.KmADHNADH*x[0]*x[6])/(self.KiADHNAD*self.KiADHNADH*self.KmADHACE) + x[7]/self.KiADHNADH + (self.ETOH*self.KmADHNAD*x[7])/(self.KiADHNAD*self.KiADHNADH*self.KmADHETOH) + (x[0]*x[7])/(self.KiADHNADH*self.KmADHACE) + (self.ETOH*x[0]*x[7])/(self.KiADHETOH*self.KiADHNADH*self.KmADHACE))))

    def v_16(self, x):
        # Glycerol 3-phosphate dehydrogenase
        # TRIO + NADH => NAD + GLY
        return (self.VmG3PDH*(-((self.GLY*x[6])/self.KeqG3PDH) + (x[7]*x[13])/(1 + self.KeqTPI)))/(self.KmG3PDHDHAP*self.KmG3PDHNADH*(1 + x[6]/self.KmG3PDHNAD + x[7]/self.KmG3PDHNADH)*(1 + self.GLY/self.KmG3PDHGLY + x[13]/((1 + self.KeqTPI)*self.KmG3PDHDHAP)))

    def v_17(self, x):
        # ATPase activity
        # Prb <=> X
        return (self.KATPASE*(-self.SUMAXP + x[12] - 4*self.KeqAK*x[12] + (self.SUMAXP**2 - 2*self.SUMAXP*x[12] + 8*self.KeqAK*self.SUMAXP*x[12] + x[12]**2 - 4*self.KeqAK*x[12]**2)**0.5))/(2 - 8*self.KeqAK)

    def dACE_dt(self, x):
        return 1.0 * self.v_12(x) - 1.0 * self.v_15(x) - 2.0 * self.v_13(x)

    def dBPG_dt(self, x):
        return 1.0 * self.v_7(x) - 1.0 * self.v_8(x)

    def dF16BP_dt(self, x):
        return 1.0 * self.v_5(x) - 1.0 * self.v_6(x)

    def dF6P_dt(self, x):
        return 1.0 * self.v_2(x) - 1.0 * self.v_5(x)

    def dG6P_dt(self, x):
        return 1.0 * self.v_1(x) - 2.0 * self.v_4(x) - 1.0 * self.v_3(x) - 1.0 * self.v_2(x)

    def dGLCi_dt(self, x):
        return 1.0 * self.v_14(x) - 1.0 * self.v_1(x)

    def dNAD_dt(self, x):
        return 1.0 * self.v_15(x) + 1.0 * self.v_16(x) - 1.0 * self.v_7(x) - 3.0 * self.v_13(x)

    def dNADH_dt(self, x):
        return 1.0 * self.v_7(x) + 3.0 * self.v_13(x) - 1.0 * self.v_15(x) - 1.0 * self.v_16(x)

    def dP2G_dt(self, x):
        return 1.0 * self.v_9(x) - 1.0 * self.v_10(x)

    def dP3G_dt(self, x):
        return 1.0 * self.v_8(x) - 1.0 * self.v_9(x)

    def dPEP_dt(self, x):
        return 1.0 * self.v_10(x) - 1.0 * self.v_11(x)

    def dPYR_dt(self, x):
        return 1.0 * self.v_11(x) - 1.0 * self.v_12(x)

    def dPrb_dt(self, x):
        return 1.0 * self.v_8(x) + 1.0 * self.v_11(x) \
            - 1.0 * self.v_4(x) - 1.0 * self.v_3(x) \
            - 1.0 * self.v_17(x) - 1.0 * self.v_1(x) \
            - 1.0 * self.v_5(x) - 4 * self.v_13(x)

    def dTRIO_dt(self, x):
        return 2.0 * self.v_6(x) - 1.0 * self.v_16(x) - 1.0 * self.v_7(x)

    def dx_dt(self, x):
        """ Calculate the time derivative of the species concentrations

        Args:
            x (:obj:`numpy.array`): species concentrations (mM)

        Returns:
            :obj:`numpy.array`: time derivative of the species concentrations (mM min\ :sup:`-1`)
        """
        return numpy.array([
            self.dACE_dt(x),
            self.dBPG_dt(x),
            self.dF16BP_dt(x),
            self.dF6P_dt(x),
            self.dG6P_dt(x),
            self.dGLCi_dt(x),
            self.dNAD_dt(x),
            self.dNADH_dt(x),
            self.dP2G_dt(x),
            self.dP3G_dt(x),
            self.dPEP_dt(x),
            self.dPYR_dt(x),
            self.dPrb_dt(x),
            self.dTRIO_dt(x),
        ])

    def simulate(self, t_0=0, t_end=20.0, t_step=0.2):
        """ Simulate the model

        Args:
            t_0 (:obj:`float`, optional): start time (min)
            t_end (:obj:`float`, optional): end time (min)
            t_step (:obj:`float`, optional): time step to record predicted concentrations (min)

        Returns:
            :obj:`tuple`:
                * :obj:`numpy.array`: time (min)
                * :obj:`numpy.array`: DHAP concentration (mM)
        """
        assert ((t_end - t_0) / t_step % 1 == 0)
        t = numpy.linspace(t_0, t_end, int((t_end - t_0) / t_step) + 1)
        x = odeint(lambda x, t: self.dx_dt(x), self.x_0, t)
        trio = x[:, -1]

        dhap = trio / (self.KeqTPI + 1)

        return (t, dhap)

    def plot_simulation_results(self, t, dhap):
        """ Plot simulation results

        Args:
            t (:obj:`numpy.array`): time (min)
            dhap (:obj:`numpy.array`): DHAP concentration (mM)

        Returns:
            :obj:`matplotlib.figure.Figure`: figure
        """
        fig, axes = pyplot.subplots(nrows=1, ncols=1)

        axes.plot(t, dhap, label='DHAP')
        axes.set_xlim((t[0], t[-1]))
        axes.set_ylim((0, 5.0))
        axes.set_xlabel('Time (min)')
        axes.set_ylabel('Concentration (mM)')
        axes.legend()

        return fig


class GlycerolModel(object):
    """ Glycerol synthesis model (Cronwright et al., 2002)

    Based on the `version from JWS Online <http://jjj.biochem.sun.ac.za/models/cronwright/>`_

    Attributes:
        ADP (:obj:`float`): ADP concentration (mM)
        ATP (:obj:`float`): ATP concentration (mM)
        DHAP (:obj:`float`): DHAP concentration (mM)
        GLY (:obj:`float`): GLY concentration (mM)
        F16BP (:obj:`float`): F16BP concentration (mM)
        NAD (:obj:`float`): NAD concentration (mM)
        NADH (:obj:`float`): NADH concentration (mM)
        Phi (:obj:`float`): Pi concentration (mM)
 
        V2 (:obj:`float`): forward rate constant (mM min\ :sup:`-1`)
        Vf1 (:obj:`float`): reverse rate constant (mM min\ :sup:`-1`)

        K1adp (:obj:`float`): ADP forward affinity constant (mM)
        K1atp (:obj:`float`): ATP forward affinity constant (mM)
        K1dhap (:obj:`float`): DHAP forward affinity constant (mM)
        K1f16bp (:obj:`float`): F16BP forward affinity constant (mM)
        K1g3p (:obj:`float`): G3P forward affinity constant (mM)
        K1nad (:obj:`float`): NAD forward affinity constant (mM)
        K1nadh (:obj:`float`): NADH forward affinity constant (mM)
        K2g3p (:obj:`float`): G3P reverse affinity constant (mM)
        K2phi (:obj:`float`): Pi reverse affinity constant (mM)
        Keq1 (:obj:`float`): Equilibrium constant (dimensionless)

        g3p_0 (:obj:`numpy.array`): initial G3P concentration (mM)
        x_0 (:obj:`numpy.array`): initial species concentrations (mM)
    """
    ADP = 2.17
    ATP = 2.37
    DHAP = 0.59
    F16BP = 6.01
    GLY = 0.0
    NAD = 1.45
    NADH = 1.87
    Phi = 1.0

    V2 = 53.0
    Vf1 = 47.0

    K1adp = 2.0
    K1atp = 0.73
    K1dhap = 0.54
    K1f16bp = 4.8
    K1g3p = 1.2
    K1nad = 0.93
    K1nadh = 0.023
    K2g3p = 3.5
    K2phi = 1.0

    Keq1 = 10000.0

    g3p_0 = 0

    @property
    def x_0(self):
        return numpy.array([self.g3p_0])

    def v_1(self, x):
        """ Calculate the rate of Glycerol 3-phosphate dehydrogenase (DHAP <=> G3P)

        Args:
            x (:obj:`numpy.array`): species concentrations (mM)

        Returns:
            :obj:`float`: rate of Glycerol 3-phosphate dehydrogenase (mM min\ :sup:`-1`)
        """
        return (self.Vf1 * (self.DHAP * self.NADH - (self.NAD * x[0]) / self.Keq1)) / \
            (self.K1dhap * (1 + self.ADP/self.K1adp + self.ATP / self.K1atp + self.F16BP / self.K1f16bp)
             * self.K1nadh * (1 + self.NAD/self.K1nad + self.NADH / self.K1nadh) *
             (1 + self.DHAP / self.K1dhap + x[0] / self.K1g3p))

    def v_2(self, x):
        """ Calculate the rate of Glycerol 3-phosphatase (G3P <=> Gly)

        Args:
            x (:obj:`numpy.array`): species concentrations (mM)

        Returns:
            :obj:`float`: rate of Glycerol 3-phosphatase (mM min\ :sup:`-1`)
        """
        return self.V2 * x[0] / (self.K2g3p * (1 + self.Phi / self.K2phi) * (1 + x[0] / self.K2g3p))

    def dg3p_dt(self, x):
        """ Calculate time derivative of the G3P concentration

        Args:
            x (:obj:`numpy.array`): species concentrations (mM)

        Returns:
            :obj:`float`: time derivative of the G3P concentration (mM min\ :sup:`-1`)
        """
        return self.v_1(x) - self.v_2(x)

    def dx_dt(self, x):
        """ Calculate the time derivative of the species concentrations

        Args:
            x (:obj:`numpy.array`): species concentrations (mM)

        Returns:
            :obj:`numpy.array`: time derivative of the species concentrations (mM min\ :sup:`-1`)
        """

        return numpy.array([self.dg3p_dt(x)])

    def simulate(self, t_0=0, t_end=20.0, t_step=0.2):
        """ Simulate the model

        Args:
            t_0 (:obj:`float`, optional): start time (min)
            t_end (:obj:`float`, optional): end time (min)
            t_step (:obj:`float`, optional): time step to record predicted concentrations (min)

        Returns:
            :obj:`tuple`:
                * :obj:`numpy.array`: time (min)
                * :obj:`numpy.array`: DHAP concentration (mM)
                * :obj:`numpy.array`: G3P concentration (mM)
        """
        assert ((t_end - t_0) / t_step % 1 == 0)
        t = numpy.linspace(t_0, t_end, int((t_end - t_0) / t_step) + 1)
        dhap = self.DHAP * numpy.ones(t.shape)
        g3p = odeint(lambda x, t: self.dx_dt(x), self.x_0, t)

        return (t, dhap, g3p)

    def plot_simulation_results(self, t, dhap, g3p):
        """ Plot simulation results

        Args:
            t (:obj:`numpy.array`): time (min)
            dhap (:obj:`numpy.array`): DHAP concentration (mM)
            g3p (:obj:`numpy.array`): G3P concentration (mM)

        Returns:
            :obj:`matplotlib.figure.Figure`: figure
        """
        fig, axes = pyplot.subplots(nrows=1, ncols=1)

        axes.plot(t, dhap, label='DHAP')
        axes.plot(t, g3p, label='G3P')
        axes.set_xlim((t[0], t[-1]))
        axes.set_ylim((0, 0.6))
        axes.set_xlabel('Time (min)')
        axes.set_ylabel('Concentration (mM)')
        axes.legend()

        return fig


class MergedModel(object):
    """ Merged model

    Attributes:
        glycolysis_model (:obj:`GlycolysisModel`): glycolysis model
        glycerol_model (:obj:`GlycerolModel`): glycerol model

        x_0 (:obj:`numpy.array`): initial species concentrations (mM)
    """

    def __init__(self):
        self.glycolysis_model = GlycolysisModel()
        self.glycerol_model = GlycerolModel()

    @property
    def x_0(self):
        return numpy.array([
            self.glycolysis_model.ACE_0,
            self.glycolysis_model.BPG_0,
            self.glycolysis_model.F16BP_0,
            self.glycolysis_model.F6P_0,
            self.glycolysis_model.G6P_0,
            self.glycolysis_model.GLCi_0,
            self.glycolysis_model.NAD_0,
            self.glycolysis_model.NADH_0,
            self.glycolysis_model.P2G_0,
            self.glycolysis_model.P3G_0,
            self.glycolysis_model.PEP_0,
            self.glycolysis_model.PYR_0,
            self.glycolysis_model.Prb_0,
            self.glycolysis_model.TRIO_0,
            self.glycerol_model.g3p_0,
        ])

    def v_18(self, x):
        # Glycerol 3-phosphate dehydrogenase (DHAP <=> G3P)
        ATP = x[12] * 2 / 3
        ADP = x[12] / 3
        DHAP = x[13] / (self.glycolysis_model.KeqTPI + 1)
        F16BP = x[2]
        G3P = x[14]
        NAD = x[6]
        NADH = x[7]
        mdl = self.glycerol_model
        return (mdl.Vf1 * (DHAP * NADH - (NAD * G3P) / mdl.Keq1)) / \
            (mdl.K1dhap * (1 + ADP / mdl.K1adp + ATP / mdl.K1atp + F16BP / mdl.K1f16bp)
             * mdl.K1nadh * (1 + NAD / mdl.K1nad + NADH / mdl.K1nadh) *
             (1 + DHAP / mdl.K1dhap + G3P / mdl.K1g3p))

    def v_19(self, x):
        # Glycerol 3-phosphatase (G3P <=> Gly)
        return self.glycerol_model.v_2(x[14:15])

    def dx_dt(self, x):
        """ Calculate the time derivative of the species concentrations

        Args:
            x (:obj:`numpy.array`): species concentrations (mM)

        Returns:
            :obj:`numpy.array`: time derivative of the species concentrations (mM min\ :sup:`-1`)
        """
        dx_dt = numpy.concatenate((
            self.glycolysis_model.dx_dt(x[0:-1]),
            numpy.array([1.0 * self.v_18(x) - 1.0 * self.v_19(x)]),
        ))
        dx_dt[6] += -1.0 * self.glycolysis_model.v_16(x[0:-1]) + 1.0 * self.v_18(x)
        dx_dt[7] += 1.0 * self.glycolysis_model.v_16(x[0:-1]) - 1.0 * self.v_18(x)
        dx_dt[13] += 1.0 * self.glycolysis_model.v_16(x[0:-1]) - 1.0 * self.v_18(x)
        return dx_dt

    def simulate(self, t_0=0, t_end=20.0, t_step=0.2):
        """ Simulate the model

        Args:
            t_0 (:obj:`float`, optional): start time (min)
            t_end (:obj:`float`, optional): end time (min)
            t_step (:obj:`float`, optional): time step to record predicted concentrations (min)

        Returns:
            :obj:`tuple`:
                * :obj:`numpy.array`: time (min)
                * :obj:`numpy.array`: DHAP concentration (mM)
                * :obj:`numpy.array`: G3P concentration (mM)
        """
        assert ((t_end - t_0) / t_step % 1 == 0)
        t = numpy.linspace(t_0, t_end, int((t_end - t_0) / t_step) + 1)
        x = odeint(lambda x, t: self.dx_dt(x), self.x_0, t)

        trio = x[:, -2]
        dhap = trio / (self.glycolysis_model.KeqTPI + 1)
        g3p = x[:, -1]

        return (t, dhap, g3p)


def main(out_dir=None):
    """ Simulate individual models and combined model, plot results, and save plots

    Args:
        out_dir (:obj:`str`, optional): path to directory to save results
    """

    out_dir = out_dir or os.path.join(os.path.dirname(__file__), '..', '..', 'docs', 'cell_modeling', 'model_composition')

    # make output directory if it doesn't already exist
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)

    # simulate the glycolysis model
    glycolysis_model = GlycolysisModel()
    t, glycolysis_model_dhap = glycolysis_model.simulate()
    fig = glycolysis_model.plot_simulation_results(t, glycolysis_model_dhap)
    # pyplot.show(block=False)
    filename = os.path.join(out_dir, 'glycolysis-model.png')
    fig.savefig(filename, transparent=True, bbox_inches='tight')
    pyplot.close(fig)

    # simulate the glycerol model
    glycerol_model = GlycerolModel()
    t, glycerol_model_dhap, glycerol_model_g3p = glycerol_model.simulate()
    fig = glycerol_model.plot_simulation_results(t, glycerol_model_dhap, glycerol_model_g3p)
    # pyplot.show(block=False)
    filename = os.path.join(out_dir, 'glycerol-model.png')
    fig.savefig(filename, transparent=True, bbox_inches='tight')
    pyplot.close(fig)

    # simulate merged model
    merged_model = MergedModel()
    t, merged_model_dhap, merged_model_g3p = merged_model.simulate()

    # compare results
    fig, axes = pyplot.subplots(nrows=2, ncols=1)

    axes[0].plot(t, merged_model_dhap, label='Merged')
    axes[0].plot(t, glycerol_model_dhap, label='Glycerol synthesis')
    axes[0].plot(t, glycolysis_model_dhap, label='Glycolysis')
    axes[0].set_xlim((t[0], t[-1]))
    axes[0].set_ylim((0, 5.))
    axes[0].set_ylabel('DHAP (mM)')
    axes[0].legend()

    axes[1].plot(t, merged_model_g3p, label='Merged')
    axes[1].plot(t, glycerol_model_g3p, label='Glycerol synthesis model')
    axes[1].set_xlim((t[0], t[-1]))
    axes[1].set_ylim((0, 0.8))
    axes[1].set_xlabel('Time (min)')
    axes[1].set_ylabel('G3P (mM)')

    # pyplot.show(block=False)
    filename = os.path.join(out_dir, 'merged-model.png')
    fig.savefig(filename, transparent=True, bbox_inches='tight')
    pyplot.close(fig)
