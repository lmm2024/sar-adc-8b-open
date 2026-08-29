module sar_ctrl (busy,
    clk,
    clk_cmp,
    cmp,
    cmp_n,
    done,
    hold,
    rst_n,
    sample,
    start,
    dac_code,
    dac_code_n,
    result);
 output busy;
 input clk;
 output clk_cmp;
 input cmp;
 input cmp_n;
 output done;
 output hold;
 input rst_n;
 output sample;
 input start;
 output [7:0] dac_code;
 output [7:0] dac_code_n;
 output [7:0] result;

 wire _000_;
 wire _001_;
 wire _002_;
 wire _003_;
 wire _004_;
 wire _005_;
 wire _006_;
 wire _007_;
 wire _008_;
 wire _009_;
 wire clknet_0_clk;
 wire _011_;
 wire _012_;
 wire _013_;
 wire _014_;
 wire _015_;
 wire _016_;
 wire _017_;
 wire _018_;
 wire _019_;
 wire _020_;
 wire _021_;
 wire _022_;
 wire _023_;
 wire _024_;
 wire _025_;
 wire _026_;
 wire _027_;
 wire _028_;
 wire _029_;
 wire _030_;
 wire _031_;
 wire _032_;
 wire _033_;
 wire _034_;
 wire _035_;
 wire _036_;
 wire _037_;
 wire _038_;
 wire _039_;
 wire _040_;
 wire _041_;
 wire _042_;
 wire _043_;
 wire _044_;
 wire _045_;
 wire _046_;
 wire _047_;
 wire _048_;
 wire _049_;
 wire _050_;
 wire _051_;
 wire _052_;
 wire _053_;
 wire _054_;
 wire _055_;
 wire _056_;
 wire _057_;
 wire _058_;
 wire _059_;
 wire _060_;
 wire _061_;
 wire _062_;
 wire _063_;
 wire _064_;
 wire _065_;
 wire _066_;
 wire _067_;
 wire _068_;
 wire _069_;
 wire _070_;
 wire _071_;
 wire _072_;
 wire _073_;
 wire _074_;
 wire _075_;
 wire _076_;
 wire _077_;
 wire _078_;
 wire _079_;
 wire _080_;
 wire _081_;
 wire _082_;
 wire _083_;
 wire _084_;
 wire _085_;
 wire _086_;
 wire _087_;
 wire _088_;
 wire _089_;
 wire _090_;
 wire _091_;
 wire _092_;
 wire _093_;
 wire _094_;
 wire _095_;
 wire _096_;
 wire _097_;
 wire _098_;
 wire _099_;
 wire _100_;
 wire _101_;
 wire _102_;
 wire _103_;
 wire _104_;
 wire _105_;
 wire _106_;
 wire _107_;
 wire _108_;
 wire _109_;
 wire _110_;
 wire _111_;
 wire _112_;
 wire \bit_idx[0] ;
 wire \bit_idx[1] ;
 wire \bit_idx[2] ;
 wire net5;
 wire net48;
 wire net1;
 wire net2;
 wire cmp_q;
 wire cmp_qb;
 wire net7;
 wire net8;
 wire net9;
 wire net10;
 wire net11;
 wire net12;
 wire net13;
 wire net14;
 wire net15;
 wire net16;
 wire net17;
 wire net18;
 wire net19;
 wire net20;
 wire net21;
 wire net22;
 wire net23;
 wire net24;
 wire last_n;
 wire net25;
 wire net26;
 wire net27;
 wire net28;
 wire net29;
 wire net30;
 wire net31;
 wire net32;
 wire net3;
 wire net33;
 wire sample_p;
 wire net4;
 wire start_q;
 wire \state[0] ;
 wire \state[1] ;
 wire \state[2] ;
 wire net34;
 wire net35;
 wire net36;
 wire net37;
 wire net38;
 wire net39;
 wire net40;
 wire net41;
 wire net42;
 wire net43;
 wire net44;
 wire net45;
 wire net46;
 wire net47;
 wire clknet_2_0__leaf_clk;
 wire clknet_2_1__leaf_clk;
 wire clknet_2_2__leaf_clk;
 wire clknet_2_3__leaf_clk;

 sg13g2_fill_2 FILLER_0_0 ();
 sg13g2_fill_1 FILLER_0_33 ();
 sg13g2_fill_1 FILLER_0_46 ();
 sg13g2_fill_1 FILLER_0_55 ();
 sg13g2_fill_2 FILLER_0_80 ();
 sg13g2_fill_1 FILLER_10_0 ();
 sg13g2_fill_1 FILLER_10_15 ();
 sg13g2_fill_2 FILLER_10_24 ();
 sg13g2_fill_2 FILLER_10_36 ();
 sg13g2_fill_2 FILLER_10_47 ();
 sg13g2_fill_2 FILLER_10_5 ();
 sg13g2_decap_8 FILLER_10_58 ();
 sg13g2_fill_2 FILLER_10_65 ();
 sg13g2_decap_4 FILLER_10_76 ();
 sg13g2_fill_2 FILLER_10_80 ();
 sg13g2_fill_2 FILLER_11_34 ();
 sg13g2_fill_1 FILLER_11_61 ();
 sg13g2_fill_2 FILLER_11_75 ();
 sg13g2_fill_1 FILLER_11_77 ();
 sg13g2_decap_8 FILLER_12_27 ();
 sg13g2_decap_8 FILLER_12_42 ();
 sg13g2_fill_1 FILLER_12_49 ();
 sg13g2_decap_8 FILLER_12_59 ();
 sg13g2_fill_2 FILLER_12_79 ();
 sg13g2_fill_1 FILLER_12_81 ();
 sg13g2_decap_4 FILLER_13_20 ();
 sg13g2_fill_2 FILLER_13_24 ();
 sg13g2_fill_1 FILLER_13_31 ();
 sg13g2_fill_1 FILLER_13_37 ();
 sg13g2_fill_1 FILLER_13_4 ();
 sg13g2_decap_8 FILLER_13_45 ();
 sg13g2_fill_2 FILLER_13_52 ();
 sg13g2_fill_1 FILLER_13_81 ();
 sg13g2_fill_2 FILLER_13_9 ();
 sg13g2_fill_1 FILLER_14_39 ();
 sg13g2_fill_2 FILLER_15_0 ();
 sg13g2_decap_8 FILLER_15_17 ();
 sg13g2_fill_1 FILLER_15_24 ();
 sg13g2_decap_8 FILLER_15_29 ();
 sg13g2_fill_2 FILLER_15_36 ();
 sg13g2_fill_1 FILLER_15_38 ();
 sg13g2_fill_2 FILLER_15_51 ();
 sg13g2_fill_1 FILLER_15_63 ();
 sg13g2_fill_1 FILLER_15_81 ();
 sg13g2_fill_1 FILLER_16_27 ();
 sg13g2_fill_2 FILLER_16_35 ();
 sg13g2_fill_1 FILLER_16_40 ();
 sg13g2_fill_2 FILLER_16_53 ();
 sg13g2_fill_2 FILLER_17_0 ();
 sg13g2_fill_1 FILLER_17_2 ();
 sg13g2_fill_2 FILLER_17_40 ();
 sg13g2_fill_2 FILLER_18_0 ();
 sg13g2_fill_1 FILLER_18_2 ();
 sg13g2_fill_1 FILLER_18_49 ();
 sg13g2_decap_8 FILLER_19_0 ();
 sg13g2_fill_1 FILLER_19_11 ();
 sg13g2_decap_4 FILLER_19_30 ();
 sg13g2_decap_4 FILLER_19_39 ();
 sg13g2_fill_1 FILLER_19_51 ();
 sg13g2_decap_4 FILLER_19_7 ();
 sg13g2_fill_1 FILLER_1_46 ();
 sg13g2_decap_4 FILLER_20_39 ();
 sg13g2_fill_2 FILLER_20_48 ();
 sg13g2_fill_2 FILLER_21_27 ();
 sg13g2_fill_1 FILLER_21_29 ();
 sg13g2_decap_4 FILLER_21_78 ();
 sg13g2_decap_8 FILLER_22_0 ();
 sg13g2_decap_8 FILLER_22_25 ();
 sg13g2_decap_8 FILLER_22_32 ();
 sg13g2_decap_8 FILLER_22_39 ();
 sg13g2_decap_8 FILLER_22_46 ();
 sg13g2_decap_8 FILLER_22_53 ();
 sg13g2_decap_8 FILLER_22_60 ();
 sg13g2_decap_8 FILLER_22_67 ();
 sg13g2_decap_4 FILLER_22_7 ();
 sg13g2_decap_8 FILLER_22_74 ();
 sg13g2_fill_1 FILLER_22_81 ();
 sg13g2_fill_1 FILLER_2_56 ();
 sg13g2_fill_1 FILLER_4_0 ();
 sg13g2_fill_1 FILLER_4_45 ();
 sg13g2_fill_1 FILLER_5_27 ();
 sg13g2_fill_2 FILLER_5_72 ();
 sg13g2_fill_2 FILLER_6_49 ();
 sg13g2_fill_1 FILLER_7_4 ();
 sg13g2_fill_1 FILLER_8_4 ();
 sg13g2_fill_1 FILLER_8_40 ();
 sg13g2_fill_2 FILLER_8_54 ();
 sg13g2_fill_1 FILLER_8_56 ();
 sg13g2_fill_2 FILLER_8_62 ();
 sg13g2_fill_1 FILLER_8_81 ();
 sg13g2_fill_1 FILLER_8_9 ();
 sg13g2_fill_2 FILLER_9_54 ();
 sg13g2_fill_2 FILLER_9_61 ();
 sg13g2_fill_1 FILLER_9_81 ();
 sg13g2_inv_1 _113_ (.Y(net14),
    .A(_009_));
 sg13g2_inv_1 _114_ (.Y(net13),
    .A(_008_));
 sg13g2_inv_1 _115_ (.Y(net12),
    .A(_007_));
 sg13g2_inv_1 _116_ (.Y(net11),
    .A(_006_));
 sg13g2_inv_1 _117_ (.Y(net10),
    .A(_005_));
 sg13g2_inv_1 _118_ (.Y(net9),
    .A(_004_));
 sg13g2_inv_1 _119_ (.Y(net8),
    .A(_003_));
 sg13g2_inv_1 _120_ (.Y(net7),
    .A(_002_));
 sg13g2_inv_1 _121_ (.Y(net24),
    .A(sample_p));
 sg13g2_inv_1 _122_ (.Y(_106_),
    .A(\state[0] ));
 sg13g2_inv_1 _123_ (.Y(_107_),
    .A(net42));
 sg13g2_inv_1 _124__47 (.Y(net47),
    .A(clknet_2_2__leaf_clk));
 sg13g2_inv_1 _125_ (.Y(_108_),
    .A(cmp_q));
 sg13g2_inv_1 _126_ (.Y(_109_),
    .A(net5));
 sg13g2_nand2_1 _127_ (.Y(net19),
    .A(net11),
    .B(net38));
 sg13g2_nand2_1 _128_ (.Y(net20),
    .A(net12),
    .B(net38));
 sg13g2_nand2_1 _129_ (.Y(net21),
    .A(net13),
    .B(net38));
 sg13g2_nand2_1 _130_ (.Y(net22),
    .A(net14),
    .B(net38));
 sg13g2_nor2_1 _131_ (.A(net24),
    .B(last_n),
    .Y(net33));
 sg13g2_nor2b_1 _132_ (.A(net42),
    .B_N(\state[1] ),
    .Y(_110_));
 sg13g2_nand3b_1 _133_ (.B(\state[0] ),
    .C(\state[1] ),
    .Y(_111_),
    .A_N(net42));
 sg13g2_inv_1 _134_ (.Y(_001_),
    .A(_111_));
 sg13g2_nor2_1 _135_ (.A(\state[1] ),
    .B(\state[0] ),
    .Y(_112_));
 sg13g2_or2_1 _136_ (.X(_036_),
    .B(\state[0] ),
    .A(\state[1] ));
 sg13g2_nand2_1 _137_ (.Y(_037_),
    .A(net42),
    .B(_112_));
 sg13g2_nor2_1 _138_ (.A(net39),
    .B(net40),
    .Y(_038_));
 sg13g2_nor2_1 _139_ (.A(net39),
    .B(net41),
    .Y(_039_));
 sg13g2_or3_1 _140_ (.A(net39),
    .B(net41),
    .C(net40),
    .X(_040_));
 sg13g2_or3_1 _141_ (.A(_107_),
    .B(_036_),
    .C(_040_),
    .X(_041_));
 sg13g2_inv_1 _142_ (.Y(_000_),
    .A(net35));
 sg13g2_nand2_1 _143_ (.Y(net15),
    .A(net7),
    .B(net38));
 sg13g2_nand2_1 _144_ (.Y(net18),
    .A(net10),
    .B(net38));
 sg13g2_nand2_1 _145_ (.Y(net17),
    .A(net9),
    .B(net38));
 sg13g2_nand2_1 _146_ (.Y(net16),
    .A(net8),
    .B(net38));
 sg13g2_nand2_1 _147_ (.Y(_042_),
    .A(net32),
    .B(net35));
 sg13g2_o21ai_1 _148_ (.B1(_042_),
    .Y(_011_),
    .A1(_009_),
    .A2(net35));
 sg13g2_nand3_1 _149_ (.B(_112_),
    .C(_040_),
    .A(net42),
    .Y(_043_));
 sg13g2_nor3_1 _150_ (.A(\state[1] ),
    .B(\state[0] ),
    .C(net42),
    .Y(_044_));
 sg13g2_nand2b_1 _151_ (.Y(_045_),
    .B(_044_),
    .A_N(net4));
 sg13g2_a21oi_1 _152_ (.A1(\state[1] ),
    .A2(\state[2] ),
    .Y(_046_),
    .B1(\state[0] ));
 sg13g2_and3_1 _153_ (.X(_012_),
    .A(_043_),
    .B(_045_),
    .C(_046_));
 sg13g2_nor2b_1 _154_ (.A(\state[1] ),
    .B_N(\state[0] ),
    .Y(_047_));
 sg13g2_and2_1 _155_ (.A(\state[2] ),
    .B(_047_),
    .X(_048_));
 sg13g2_nor2_1 _156_ (.A(net4),
    .B(start_q),
    .Y(_049_));
 sg13g2_nand3b_1 _157_ (.B(_047_),
    .C(\state[2] ),
    .Y(_050_),
    .A_N(_049_));
 sg13g2_a22oi_1 _158_ (.Y(_051_),
    .B1(_047_),
    .B2(_107_),
    .A2(_110_),
    .A1(_106_));
 sg13g2_nand2_1 _159_ (.Y(_013_),
    .A(_050_),
    .B(_051_));
 sg13g2_a22oi_1 _160_ (.Y(_052_),
    .B1(_112_),
    .B2(net42),
    .A2(_110_),
    .A1(\state[0] ));
 sg13g2_inv_1 _161_ (.Y(_014_),
    .A(net34));
 sg13g2_nand3_1 _162_ (.B(_045_),
    .C(_050_),
    .A(_043_),
    .Y(_053_));
 sg13g2_nor3_1 _163_ (.A(_044_),
    .B(_048_),
    .C(_014_),
    .Y(_054_));
 sg13g2_o21ai_1 _164_ (.B1(sample_p),
    .Y(_055_),
    .A1(_053_),
    .A2(_054_));
 sg13g2_o21ai_1 _165_ (.B1(_055_),
    .Y(_015_),
    .A1(_036_),
    .A2(_053_));
 sg13g2_nor2b_1 _166_ (.A(start_q),
    .B_N(_044_),
    .Y(_056_));
 sg13g2_nor3_1 _167_ (.A(_048_),
    .B(_049_),
    .C(_056_),
    .Y(_016_));
 sg13g2_and2_1 _168_ (.A(net37),
    .B(_014_),
    .X(_057_));
 sg13g2_mux2_1 _169_ (.A0(_057_),
    .A1(_037_),
    .S(net41),
    .X(_017_));
 sg13g2_or2_1 _170_ (.X(_058_),
    .B(net40),
    .A(net41));
 sg13g2_nand2_1 _171_ (.Y(_059_),
    .A(\bit_idx[0] ),
    .B(net40));
 sg13g2_nand4_1 _172_ (.B(_112_),
    .C(_058_),
    .A(net42),
    .Y(_060_),
    .D(_059_));
 sg13g2_a22oi_1 _173_ (.Y(_061_),
    .B1(_057_),
    .B2(_060_),
    .A2(net34),
    .A1(\bit_idx[1] ));
 sg13g2_inv_1 _174_ (.Y(_018_),
    .A(_061_));
 sg13g2_o21ai_1 _175_ (.B1(net39),
    .Y(_062_),
    .A1(net41),
    .A2(\bit_idx[1] ));
 sg13g2_o21ai_1 _176_ (.B1(_043_),
    .Y(_063_),
    .A1(net39),
    .A2(_057_));
 sg13g2_nand2_1 _177_ (.Y(_019_),
    .A(_062_),
    .B(_063_));
 sg13g2_nand2_1 _178_ (.Y(_064_),
    .A(net4),
    .B(_044_));
 sg13g2_and2_1 _179_ (.A(net34),
    .B(_064_),
    .X(_065_));
 sg13g2_nand2_1 _180_ (.Y(_066_),
    .A(net34),
    .B(_064_));
 sg13g2_o21ai_1 _181_ (.B1(_066_),
    .Y(_067_),
    .A1(_038_),
    .A2(_052_));
 sg13g2_a21o_1 _182_ (.A2(_067_),
    .A1(_002_),
    .B1(_001_),
    .X(_020_));
 sg13g2_nand2_1 _183_ (.Y(_068_),
    .A(_003_),
    .B(_065_));
 sg13g2_or2_1 _184_ (.X(_069_),
    .B(_038_),
    .A(_003_));
 sg13g2_a21oi_1 _185_ (.A1(cmp_q),
    .A2(_038_),
    .Y(_070_),
    .B1(_039_));
 sg13g2_a21oi_1 _186_ (.A1(_069_),
    .A2(_070_),
    .Y(_071_),
    .B1(_037_));
 sg13g2_o21ai_1 _187_ (.B1(_068_),
    .Y(_021_),
    .A1(net34),
    .A2(_071_));
 sg13g2_a21oi_1 _188_ (.A1(net40),
    .A2(_039_),
    .Y(_072_),
    .B1(_004_));
 sg13g2_and3_1 _189_ (.X(_073_),
    .A(net40),
    .B(cmp_q),
    .C(_039_));
 sg13g2_a21oi_1 _190_ (.A1(_058_),
    .A2(_059_),
    .Y(_074_),
    .B1(net39));
 sg13g2_nor3_1 _191_ (.A(_072_),
    .B(_073_),
    .C(_074_),
    .Y(_075_));
 sg13g2_o21ai_1 _192_ (.B1(_014_),
    .Y(_076_),
    .A1(_037_),
    .A2(_075_));
 sg13g2_o21ai_1 _193_ (.B1(_076_),
    .Y(_022_),
    .A1(net9),
    .A2(_066_));
 sg13g2_nor2_1 _194_ (.A(\bit_idx[2] ),
    .B(_059_),
    .Y(_077_));
 sg13g2_mux2_1 _195_ (.A0(_005_),
    .A1(_108_),
    .S(_077_),
    .X(_078_));
 sg13g2_a21oi_1 _196_ (.A1(_058_),
    .A2(_078_),
    .Y(_079_),
    .B1(_037_));
 sg13g2_nand2_1 _197_ (.Y(_080_),
    .A(_005_),
    .B(_065_));
 sg13g2_o21ai_1 _198_ (.B1(_080_),
    .Y(_023_),
    .A1(net34),
    .A2(_079_));
 sg13g2_nand2_1 _199_ (.Y(_081_),
    .A(_006_),
    .B(_065_));
 sg13g2_nor2b_1 _200_ (.A(\bit_idx[1] ),
    .B_N(net41),
    .Y(_082_));
 sg13g2_nand2_1 _201_ (.Y(_083_),
    .A(\bit_idx[2] ),
    .B(_082_));
 sg13g2_a21oi_1 _202_ (.A1(\bit_idx[2] ),
    .A2(_108_),
    .Y(_084_),
    .B1(_058_));
 sg13g2_a21oi_1 _203_ (.A1(net11),
    .A2(_058_),
    .Y(_085_),
    .B1(_084_));
 sg13g2_a21oi_1 _204_ (.A1(_083_),
    .A2(_085_),
    .Y(_086_),
    .B1(_037_));
 sg13g2_o21ai_1 _205_ (.B1(_081_),
    .Y(_024_),
    .A1(net34),
    .A2(_086_));
 sg13g2_nor2_1 _206_ (.A(_108_),
    .B(_062_),
    .Y(_087_));
 sg13g2_nand2_1 _207_ (.Y(_088_),
    .A(net39),
    .B(net40));
 sg13g2_o21ai_1 _208_ (.B1(_040_),
    .Y(_089_),
    .A1(net41),
    .A2(_088_));
 sg13g2_a221oi_1 _209_ (.B2(_082_),
    .C1(_089_),
    .B1(_087_),
    .A1(net12),
    .Y(_090_),
    .A2(_083_));
 sg13g2_o21ai_1 _210_ (.B1(_014_),
    .Y(_091_),
    .A1(_037_),
    .A2(_090_));
 sg13g2_o21ai_1 _211_ (.B1(_091_),
    .Y(_025_),
    .A1(net12),
    .A2(_066_));
 sg13g2_nand2_1 _212_ (.Y(_092_),
    .A(_008_),
    .B(_065_));
 sg13g2_nand3_1 _213_ (.B(net41),
    .C(net40),
    .A(net39),
    .Y(_093_));
 sg13g2_nand2b_1 _214_ (.Y(_094_),
    .B(_108_),
    .A_N(_088_));
 sg13g2_o21ai_1 _215_ (.B1(_094_),
    .Y(_095_),
    .A1(net13),
    .A2(_089_));
 sg13g2_a21oi_1 _216_ (.A1(_093_),
    .A2(_095_),
    .Y(_096_),
    .B1(_037_));
 sg13g2_o21ai_1 _217_ (.B1(_092_),
    .Y(_026_),
    .A1(net34),
    .A2(_096_));
 sg13g2_a21oi_1 _218_ (.A1(_052_),
    .A2(_064_),
    .Y(_097_),
    .B1(_093_));
 sg13g2_nor2_1 _219_ (.A(_009_),
    .B(_097_),
    .Y(_098_));
 sg13g2_a221oi_1 _220_ (.B2(cmp_q),
    .C1(_098_),
    .B1(_097_),
    .A1(_043_),
    .Y(_027_),
    .A2(_066_));
 sg13g2_a22oi_1 _221_ (.Y(_028_),
    .B1(_064_),
    .B2(_109_),
    .A2(_049_),
    .A1(_048_));
 sg13g2_nand2_1 _222_ (.Y(_099_),
    .A(net25),
    .B(net36));
 sg13g2_o21ai_1 _223_ (.B1(_099_),
    .Y(_029_),
    .A1(_108_),
    .A2(net36));
 sg13g2_nand2_1 _224_ (.Y(_100_),
    .A(net26),
    .B(net35));
 sg13g2_o21ai_1 _225_ (.B1(_100_),
    .Y(_030_),
    .A1(_003_),
    .A2(net35));
 sg13g2_nand2_1 _226_ (.Y(_101_),
    .A(net27),
    .B(net35));
 sg13g2_o21ai_1 _227_ (.B1(_101_),
    .Y(_031_),
    .A1(_004_),
    .A2(net35));
 sg13g2_nand2_1 _228_ (.Y(_102_),
    .A(net28),
    .B(net36));
 sg13g2_o21ai_1 _229_ (.B1(_102_),
    .Y(_032_),
    .A1(_005_),
    .A2(net36));
 sg13g2_nand2_1 _230_ (.Y(_103_),
    .A(net29),
    .B(net36));
 sg13g2_o21ai_1 _231_ (.B1(_103_),
    .Y(_033_),
    .A1(_006_),
    .A2(net36));
 sg13g2_nand2_1 _232_ (.Y(_104_),
    .A(net30),
    .B(net37));
 sg13g2_o21ai_1 _233_ (.B1(_104_),
    .Y(_034_),
    .A1(_007_),
    .A2(net37));
 sg13g2_nand2_1 _234_ (.Y(_105_),
    .A(net31),
    .B(net35));
 sg13g2_o21ai_1 _235_ (.B1(_105_),
    .Y(_035_),
    .A1(_008_),
    .A2(net36));
 sg13g2_inv_1 _236__48 (.Y(net48),
    .A(clknet_2_2__leaf_clk));
 sg13g2_dfrbpq_1 _237_ (.RESET_B(net45),
    .D(_020_),
    .Q(_002_),
    .CLK(clknet_2_2__leaf_clk));
 sg13g2_dfrbpq_1 _238_ (.RESET_B(net45),
    .D(_021_),
    .Q(_003_),
    .CLK(clknet_2_2__leaf_clk));
 sg13g2_dfrbpq_1 _239_ (.RESET_B(net44),
    .D(_022_),
    .Q(_004_),
    .CLK(clknet_2_0__leaf_clk));
 sg13g2_dfrbpq_1 _240_ (.RESET_B(net44),
    .D(_023_),
    .Q(_005_),
    .CLK(clknet_2_1__leaf_clk));
 sg13g2_dfrbpq_1 _241_ (.RESET_B(net44),
    .D(_024_),
    .Q(_006_),
    .CLK(clknet_2_1__leaf_clk));
 sg13g2_dfrbpq_1 _242_ (.RESET_B(net43),
    .D(_025_),
    .Q(_007_),
    .CLK(clknet_2_1__leaf_clk));
 sg13g2_dfrbpq_1 _243_ (.RESET_B(net44),
    .D(_026_),
    .Q(_008_),
    .CLK(clknet_2_0__leaf_clk));
 sg13g2_dfrbpq_1 _244_ (.RESET_B(net45),
    .D(_027_),
    .Q(_009_),
    .CLK(clknet_2_2__leaf_clk));
 sg13g2_dfrbpq_1 _245_ (.RESET_B(net45),
    .D(_028_),
    .Q(net5),
    .CLK(clknet_2_2__leaf_clk));
 sg13g2_dfrbpq_1 _246_ (.RESET_B(net44),
    .D(_029_),
    .Q(net25),
    .CLK(clknet_2_0__leaf_clk));
 sg13g2_dfrbpq_1 _247_ (.RESET_B(net43),
    .D(_030_),
    .Q(net26),
    .CLK(clknet_2_0__leaf_clk));
 sg13g2_dfrbpq_1 _248_ (.RESET_B(net43),
    .D(_031_),
    .Q(net27),
    .CLK(clknet_2_0__leaf_clk));
 sg13g2_dfrbpq_1 _249_ (.RESET_B(net43),
    .D(_032_),
    .Q(net28),
    .CLK(clknet_2_1__leaf_clk));
 sg13g2_dfrbpq_1 _250_ (.RESET_B(net43),
    .D(_033_),
    .Q(net29),
    .CLK(clknet_2_1__leaf_clk));
 sg13g2_dfrbpq_1 _251_ (.RESET_B(net44),
    .D(_034_),
    .Q(net30),
    .CLK(clknet_2_1__leaf_clk));
 sg13g2_dfrbpq_1 _252_ (.RESET_B(net43),
    .D(_035_),
    .Q(net31),
    .CLK(clknet_2_1__leaf_clk));
 sg13g2_dfrbpq_1 _253_ (.RESET_B(net43),
    .D(_011_),
    .Q(net32),
    .CLK(clknet_2_0__leaf_clk));
 sg13g2_dfrbpq_1 _254_ (.RESET_B(net45),
    .D(_012_),
    .Q(\state[0] ),
    .CLK(clknet_2_3__leaf_clk));
 sg13g2_dfrbpq_1 _255_ (.RESET_B(net46),
    .D(_013_),
    .Q(\state[1] ),
    .CLK(clknet_2_3__leaf_clk));
 sg13g2_dfrbpq_1 _256_ (.RESET_B(net46),
    .D(_014_),
    .Q(\state[2] ),
    .CLK(clknet_2_3__leaf_clk));
 sg13g2_dfrbpq_1 _257_ (.RESET_B(net46),
    .D(_015_),
    .Q(sample_p),
    .CLK(clknet_2_3__leaf_clk));
 sg13g2_dfrbpq_1 _258_ (.RESET_B(net46),
    .D(_016_),
    .Q(start_q),
    .CLK(clknet_2_2__leaf_clk));
 sg13g2_dfrbpq_1 _259_ (.RESET_B(net45),
    .D(_017_),
    .Q(\bit_idx[0] ),
    .CLK(clknet_2_3__leaf_clk));
 sg13g2_dfrbpq_1 _260_ (.RESET_B(net45),
    .D(_018_),
    .Q(\bit_idx[1] ),
    .CLK(clknet_2_3__leaf_clk));
 sg13g2_dfrbpq_1 _261_ (.RESET_B(net45),
    .D(_019_),
    .Q(\bit_idx[2] ),
    .CLK(clknet_2_3__leaf_clk));
 sg13g2_dfrbpq_1 _262_ (.RESET_B(net43),
    .D(_000_),
    .Q(net23),
    .CLK(clknet_2_0__leaf_clk));
 sg13g2_dfrbpq_1 _263_ (.RESET_B(net46),
    .D(_001_),
    .Q(last_n),
    .CLK(net48));
 sg13g2_buf_16 clkbuf_0_clk (.X(clknet_0_clk),
    .A(clk));
 sg13g2_buf_16 clkbuf_2_0__f_clk (.X(clknet_2_0__leaf_clk),
    .A(clknet_0_clk));
 sg13g2_buf_16 clkbuf_2_1__f_clk (.X(clknet_2_1__leaf_clk),
    .A(clknet_0_clk));
 sg13g2_buf_16 clkbuf_2_2__f_clk (.X(clknet_2_2__leaf_clk),
    .A(clknet_0_clk));
 sg13g2_buf_16 clkbuf_2_3__f_clk (.X(clknet_2_3__leaf_clk),
    .A(clknet_0_clk));
 sg13g2_inv_1 clkload0 (.A(clknet_2_0__leaf_clk));
 sg13g2_inv_1 clkload1 (.A(clknet_2_1__leaf_clk));
 sg13g2_inv_1 clkload2 (.A(clknet_2_3__leaf_clk));
 sg13g2_buf_1 fanout34 (.A(_052_),
    .X(net34));
 sg13g2_buf_1 fanout35 (.A(net36),
    .X(net35));
 sg13g2_buf_1 fanout36 (.A(net37),
    .X(net36));
 sg13g2_buf_1 fanout37 (.A(_041_),
    .X(net37));
 sg13g2_buf_1 fanout38 (.A(net24),
    .X(net38));
 sg13g2_buf_1 fanout39 (.A(\bit_idx[2] ),
    .X(net39));
 sg13g2_buf_1 fanout40 (.A(\bit_idx[1] ),
    .X(net40));
 sg13g2_buf_1 fanout41 (.A(\bit_idx[0] ),
    .X(net41));
 sg13g2_buf_1 fanout42 (.A(\state[2] ),
    .X(net42));
 sg13g2_buf_1 fanout43 (.A(net44),
    .X(net43));
 sg13g2_buf_1 fanout44 (.A(net3),
    .X(net44));
 sg13g2_buf_1 fanout45 (.A(net3),
    .X(net45));
 sg13g2_buf_1 fanout46 (.A(net3),
    .X(net46));
 sg13g2_buf_1 input1 (.A(cmp),
    .X(net1));
 sg13g2_buf_1 input2 (.A(cmp_n),
    .X(net2));
 sg13g2_buf_1 input3 (.A(rst_n),
    .X(net3));
 sg13g2_buf_1 input4 (.A(start),
    .X(net4));
 sg13g2_buf_1 output10 (.A(net10),
    .X(dac_code[3]));
 sg13g2_buf_1 output11 (.A(net11),
    .X(dac_code[4]));
 sg13g2_buf_1 output12 (.A(net12),
    .X(dac_code[5]));
 sg13g2_buf_1 output13 (.A(net13),
    .X(dac_code[6]));
 sg13g2_buf_1 output14 (.A(net14),
    .X(dac_code[7]));
 sg13g2_buf_1 output15 (.A(net15),
    .X(dac_code_n[0]));
 sg13g2_buf_1 output16 (.A(net16),
    .X(dac_code_n[1]));
 sg13g2_buf_1 output17 (.A(net17),
    .X(dac_code_n[2]));
 sg13g2_buf_1 output18 (.A(net18),
    .X(dac_code_n[3]));
 sg13g2_buf_1 output19 (.A(net19),
    .X(dac_code_n[4]));
 sg13g2_buf_1 output20 (.A(net20),
    .X(dac_code_n[5]));
 sg13g2_buf_1 output21 (.A(net21),
    .X(dac_code_n[6]));
 sg13g2_buf_1 output22 (.A(net22),
    .X(dac_code_n[7]));
 sg13g2_buf_1 output23 (.A(net23),
    .X(done));
 sg13g2_buf_1 output24 (.A(net24),
    .X(hold));
 sg13g2_buf_1 output25 (.A(net25),
    .X(result[0]));
 sg13g2_buf_1 output26 (.A(net26),
    .X(result[1]));
 sg13g2_buf_1 output27 (.A(net27),
    .X(result[2]));
 sg13g2_buf_1 output28 (.A(net28),
    .X(result[3]));
 sg13g2_buf_1 output29 (.A(net29),
    .X(result[4]));
 sg13g2_buf_1 output30 (.A(net30),
    .X(result[5]));
 sg13g2_buf_1 output31 (.A(net31),
    .X(result[6]));
 sg13g2_buf_1 output32 (.A(net32),
    .X(result[7]));
 sg13g2_buf_1 output33 (.A(net33),
    .X(sample));
 sg13g2_buf_1 output5 (.A(net5),
    .X(busy));
 sg13g2_buf_1 output6 (.A(net47),
    .X(clk_cmp));
 sg13g2_buf_1 output7 (.A(net7),
    .X(dac_code[0]));
 sg13g2_buf_1 output8 (.A(net8),
    .X(dac_code[1]));
 sg13g2_buf_1 output9 (.A(net9),
    .X(dac_code[2]));
 sg13g2_nand2_1 u_sr_q (.Y(cmp_q),
    .A(net2),
    .B(cmp_qb));
 sg13g2_nand2_1 u_sr_qb (.Y(cmp_qb),
    .A(net1),
    .B(cmp_q));
endmodule
