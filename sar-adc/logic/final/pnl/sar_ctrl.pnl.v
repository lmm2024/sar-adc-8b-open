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
    VDD,
    VSS,
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
 inout VDD;
 inout VSS;
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

 sg13g2_fill_2 FILLER_0_0 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_1 FILLER_0_33 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_1 FILLER_0_46 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_1 FILLER_0_55 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_2 FILLER_0_80 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_1 FILLER_10_0 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_1 FILLER_10_15 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_2 FILLER_10_24 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_2 FILLER_10_36 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_2 FILLER_10_47 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_2 FILLER_10_5 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_10_58 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_2 FILLER_10_65 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_4 FILLER_10_76 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_2 FILLER_10_80 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_2 FILLER_11_34 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_1 FILLER_11_61 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_2 FILLER_11_75 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_1 FILLER_11_77 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_12_27 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_12_42 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_1 FILLER_12_49 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_12_59 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_2 FILLER_12_79 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_1 FILLER_12_81 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_4 FILLER_13_20 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_2 FILLER_13_24 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_1 FILLER_13_31 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_1 FILLER_13_37 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_1 FILLER_13_4 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_13_45 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_2 FILLER_13_52 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_1 FILLER_13_81 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_2 FILLER_13_9 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_1 FILLER_14_39 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_2 FILLER_15_0 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_15_17 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_1 FILLER_15_24 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_15_29 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_2 FILLER_15_36 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_1 FILLER_15_38 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_2 FILLER_15_51 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_1 FILLER_15_63 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_1 FILLER_15_81 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_1 FILLER_16_27 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_2 FILLER_16_35 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_1 FILLER_16_40 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_2 FILLER_16_53 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_2 FILLER_17_0 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_1 FILLER_17_2 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_2 FILLER_17_40 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_2 FILLER_18_0 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_1 FILLER_18_2 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_1 FILLER_18_49 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_19_0 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_1 FILLER_19_11 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_4 FILLER_19_30 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_4 FILLER_19_39 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_1 FILLER_19_51 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_4 FILLER_19_7 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_1 FILLER_1_46 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_4 FILLER_20_39 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_2 FILLER_20_48 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_2 FILLER_21_27 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_1 FILLER_21_29 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_4 FILLER_21_78 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_22_0 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_22_25 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_22_32 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_22_39 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_22_46 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_22_53 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_22_60 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_22_67 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_4 FILLER_22_7 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_22_74 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_1 FILLER_22_81 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_1 FILLER_2_56 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_1 FILLER_4_0 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_1 FILLER_4_45 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_1 FILLER_5_27 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_2 FILLER_5_72 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_2 FILLER_6_49 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_1 FILLER_7_4 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_1 FILLER_8_4 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_1 FILLER_8_40 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_2 FILLER_8_54 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_1 FILLER_8_56 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_2 FILLER_8_62 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_1 FILLER_8_81 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_1 FILLER_8_9 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_2 FILLER_9_54 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_2 FILLER_9_61 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_1 FILLER_9_81 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_inv_1 _113_ (.VDD(VDD),
    .Y(net14),
    .A(_009_),
    .VSS(VSS));
 sg13g2_inv_1 _114_ (.VDD(VDD),
    .Y(net13),
    .A(_008_),
    .VSS(VSS));
 sg13g2_inv_1 _115_ (.VDD(VDD),
    .Y(net12),
    .A(_007_),
    .VSS(VSS));
 sg13g2_inv_1 _116_ (.VDD(VDD),
    .Y(net11),
    .A(_006_),
    .VSS(VSS));
 sg13g2_inv_1 _117_ (.VDD(VDD),
    .Y(net10),
    .A(_005_),
    .VSS(VSS));
 sg13g2_inv_1 _118_ (.VDD(VDD),
    .Y(net9),
    .A(_004_),
    .VSS(VSS));
 sg13g2_inv_1 _119_ (.VDD(VDD),
    .Y(net8),
    .A(_003_),
    .VSS(VSS));
 sg13g2_inv_1 _120_ (.VDD(VDD),
    .Y(net7),
    .A(_002_),
    .VSS(VSS));
 sg13g2_inv_1 _121_ (.VDD(VDD),
    .Y(net24),
    .A(sample_p),
    .VSS(VSS));
 sg13g2_inv_1 _122_ (.VDD(VDD),
    .Y(_106_),
    .A(\state[0] ),
    .VSS(VSS));
 sg13g2_inv_1 _123_ (.VDD(VDD),
    .Y(_107_),
    .A(net42),
    .VSS(VSS));
 sg13g2_inv_1 _124__47 (.VDD(VDD),
    .Y(net47),
    .A(clknet_2_2__leaf_clk),
    .VSS(VSS));
 sg13g2_inv_1 _125_ (.VDD(VDD),
    .Y(_108_),
    .A(cmp_q),
    .VSS(VSS));
 sg13g2_inv_1 _126_ (.VDD(VDD),
    .Y(_109_),
    .A(net5),
    .VSS(VSS));
 sg13g2_nand2_1 _127_ (.Y(net19),
    .A(net11),
    .B(net38),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_nand2_1 _128_ (.Y(net20),
    .A(net12),
    .B(net38),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_nand2_1 _129_ (.Y(net21),
    .A(net13),
    .B(net38),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_nand2_1 _130_ (.Y(net22),
    .A(net14),
    .B(net38),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_nor2_1 _131_ (.A(net24),
    .B(last_n),
    .Y(net33),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_nor2b_1 _132_ (.A(net42),
    .B_N(\state[1] ),
    .Y(_110_),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_nand3b_1 _133_ (.B(\state[0] ),
    .C(\state[1] ),
    .Y(_111_),
    .VDD(VDD),
    .VSS(VSS),
    .A_N(net42));
 sg13g2_inv_1 _134_ (.VDD(VDD),
    .Y(_001_),
    .A(_111_),
    .VSS(VSS));
 sg13g2_nor2_1 _135_ (.A(\state[1] ),
    .B(\state[0] ),
    .Y(_112_),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_or2_1 _136_ (.VSS(VSS),
    .VDD(VDD),
    .X(_036_),
    .B(\state[0] ),
    .A(\state[1] ));
 sg13g2_nand2_1 _137_ (.Y(_037_),
    .A(net42),
    .B(_112_),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_nor2_1 _138_ (.A(net39),
    .B(net40),
    .Y(_038_),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_nor2_1 _139_ (.A(net39),
    .B(net41),
    .Y(_039_),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_or3_1 _140_ (.A(net39),
    .B(net41),
    .C(net40),
    .X(_040_),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_or3_1 _141_ (.A(_107_),
    .B(_036_),
    .C(_040_),
    .X(_041_),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_inv_1 _142_ (.VDD(VDD),
    .Y(_000_),
    .A(net35),
    .VSS(VSS));
 sg13g2_nand2_1 _143_ (.Y(net15),
    .A(net7),
    .B(net38),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_nand2_1 _144_ (.Y(net18),
    .A(net10),
    .B(net38),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_nand2_1 _145_ (.Y(net17),
    .A(net9),
    .B(net38),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_nand2_1 _146_ (.Y(net16),
    .A(net8),
    .B(net38),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_nand2_1 _147_ (.Y(_042_),
    .A(net32),
    .B(net35),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_o21ai_1 _148_ (.B1(_042_),
    .VDD(VDD),
    .Y(_011_),
    .VSS(VSS),
    .A1(_009_),
    .A2(net35));
 sg13g2_nand3_1 _149_ (.B(_112_),
    .C(_040_),
    .A(net42),
    .Y(_043_),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_nor3_1 _150_ (.A(\state[1] ),
    .B(\state[0] ),
    .C(net42),
    .Y(_044_),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_nand2b_1 _151_ (.Y(_045_),
    .B(_044_),
    .A_N(net4),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_a21oi_1 _152_ (.VSS(VSS),
    .VDD(VDD),
    .A1(\state[1] ),
    .A2(\state[2] ),
    .Y(_046_),
    .B1(\state[0] ));
 sg13g2_and3_1 _153_ (.X(_012_),
    .A(_043_),
    .B(_045_),
    .C(_046_),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_nor2b_1 _154_ (.A(\state[1] ),
    .B_N(\state[0] ),
    .Y(_047_),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_and2_1 _155_ (.A(\state[2] ),
    .B(_047_),
    .X(_048_),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_nor2_1 _156_ (.A(net4),
    .B(start_q),
    .Y(_049_),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_nand3b_1 _157_ (.B(_047_),
    .C(\state[2] ),
    .Y(_050_),
    .VDD(VDD),
    .VSS(VSS),
    .A_N(_049_));
 sg13g2_a22oi_1 _158_ (.Y(_051_),
    .B1(_047_),
    .B2(_107_),
    .A2(_110_),
    .A1(_106_),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_nand2_1 _159_ (.Y(_013_),
    .A(_050_),
    .B(_051_),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_a22oi_1 _160_ (.Y(_052_),
    .B1(_112_),
    .B2(net42),
    .A2(_110_),
    .A1(\state[0] ),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_inv_1 _161_ (.VDD(VDD),
    .Y(_014_),
    .A(net34),
    .VSS(VSS));
 sg13g2_nand3_1 _162_ (.B(_045_),
    .C(_050_),
    .A(_043_),
    .Y(_053_),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_nor3_1 _163_ (.A(_044_),
    .B(_048_),
    .C(_014_),
    .Y(_054_),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_o21ai_1 _164_ (.B1(sample_p),
    .VDD(VDD),
    .Y(_055_),
    .VSS(VSS),
    .A1(_053_),
    .A2(_054_));
 sg13g2_o21ai_1 _165_ (.B1(_055_),
    .VDD(VDD),
    .Y(_015_),
    .VSS(VSS),
    .A1(_036_),
    .A2(_053_));
 sg13g2_nor2b_1 _166_ (.A(start_q),
    .B_N(_044_),
    .Y(_056_),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_nor3_1 _167_ (.A(_048_),
    .B(_049_),
    .C(_056_),
    .Y(_016_),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_and2_1 _168_ (.A(net37),
    .B(_014_),
    .X(_057_),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_mux2_1 _169_ (.A0(_057_),
    .A1(_037_),
    .S(net41),
    .X(_017_),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_or2_1 _170_ (.VSS(VSS),
    .VDD(VDD),
    .X(_058_),
    .B(net40),
    .A(net41));
 sg13g2_nand2_1 _171_ (.Y(_059_),
    .A(\bit_idx[0] ),
    .B(net40),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_nand4_1 _172_ (.B(_112_),
    .C(_058_),
    .A(net42),
    .Y(_060_),
    .VDD(VDD),
    .VSS(VSS),
    .D(_059_));
 sg13g2_a22oi_1 _173_ (.Y(_061_),
    .B1(_057_),
    .B2(_060_),
    .A2(net34),
    .A1(\bit_idx[1] ),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_inv_1 _174_ (.VDD(VDD),
    .Y(_018_),
    .A(_061_),
    .VSS(VSS));
 sg13g2_o21ai_1 _175_ (.B1(net39),
    .VDD(VDD),
    .Y(_062_),
    .VSS(VSS),
    .A1(net41),
    .A2(\bit_idx[1] ));
 sg13g2_o21ai_1 _176_ (.B1(_043_),
    .VDD(VDD),
    .Y(_063_),
    .VSS(VSS),
    .A1(net39),
    .A2(_057_));
 sg13g2_nand2_1 _177_ (.Y(_019_),
    .A(_062_),
    .B(_063_),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_nand2_1 _178_ (.Y(_064_),
    .A(net4),
    .B(_044_),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_and2_1 _179_ (.A(net34),
    .B(_064_),
    .X(_065_),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_nand2_1 _180_ (.Y(_066_),
    .A(net34),
    .B(_064_),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_o21ai_1 _181_ (.B1(_066_),
    .VDD(VDD),
    .Y(_067_),
    .VSS(VSS),
    .A1(_038_),
    .A2(_052_));
 sg13g2_a21o_1 _182_ (.A2(_067_),
    .A1(_002_),
    .B1(_001_),
    .X(_020_),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_nand2_1 _183_ (.Y(_068_),
    .A(_003_),
    .B(_065_),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_or2_1 _184_ (.VSS(VSS),
    .VDD(VDD),
    .X(_069_),
    .B(_038_),
    .A(_003_));
 sg13g2_a21oi_1 _185_ (.VSS(VSS),
    .VDD(VDD),
    .A1(cmp_q),
    .A2(_038_),
    .Y(_070_),
    .B1(_039_));
 sg13g2_a21oi_1 _186_ (.VSS(VSS),
    .VDD(VDD),
    .A1(_069_),
    .A2(_070_),
    .Y(_071_),
    .B1(_037_));
 sg13g2_o21ai_1 _187_ (.B1(_068_),
    .VDD(VDD),
    .Y(_021_),
    .VSS(VSS),
    .A1(net34),
    .A2(_071_));
 sg13g2_a21oi_1 _188_ (.VSS(VSS),
    .VDD(VDD),
    .A1(net40),
    .A2(_039_),
    .Y(_072_),
    .B1(_004_));
 sg13g2_and3_1 _189_ (.X(_073_),
    .A(net40),
    .B(cmp_q),
    .C(_039_),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_a21oi_1 _190_ (.VSS(VSS),
    .VDD(VDD),
    .A1(_058_),
    .A2(_059_),
    .Y(_074_),
    .B1(net39));
 sg13g2_nor3_1 _191_ (.A(_072_),
    .B(_073_),
    .C(_074_),
    .Y(_075_),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_o21ai_1 _192_ (.B1(_014_),
    .VDD(VDD),
    .Y(_076_),
    .VSS(VSS),
    .A1(_037_),
    .A2(_075_));
 sg13g2_o21ai_1 _193_ (.B1(_076_),
    .VDD(VDD),
    .Y(_022_),
    .VSS(VSS),
    .A1(net9),
    .A2(_066_));
 sg13g2_nor2_1 _194_ (.A(\bit_idx[2] ),
    .B(_059_),
    .Y(_077_),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_mux2_1 _195_ (.A0(_005_),
    .A1(_108_),
    .S(_077_),
    .X(_078_),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_a21oi_1 _196_ (.VSS(VSS),
    .VDD(VDD),
    .A1(_058_),
    .A2(_078_),
    .Y(_079_),
    .B1(_037_));
 sg13g2_nand2_1 _197_ (.Y(_080_),
    .A(_005_),
    .B(_065_),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_o21ai_1 _198_ (.B1(_080_),
    .VDD(VDD),
    .Y(_023_),
    .VSS(VSS),
    .A1(net34),
    .A2(_079_));
 sg13g2_nand2_1 _199_ (.Y(_081_),
    .A(_006_),
    .B(_065_),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_nor2b_1 _200_ (.A(\bit_idx[1] ),
    .B_N(net41),
    .Y(_082_),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_nand2_1 _201_ (.Y(_083_),
    .A(\bit_idx[2] ),
    .B(_082_),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_a21oi_1 _202_ (.VSS(VSS),
    .VDD(VDD),
    .A1(\bit_idx[2] ),
    .A2(_108_),
    .Y(_084_),
    .B1(_058_));
 sg13g2_a21oi_1 _203_ (.VSS(VSS),
    .VDD(VDD),
    .A1(net11),
    .A2(_058_),
    .Y(_085_),
    .B1(_084_));
 sg13g2_a21oi_1 _204_ (.VSS(VSS),
    .VDD(VDD),
    .A1(_083_),
    .A2(_085_),
    .Y(_086_),
    .B1(_037_));
 sg13g2_o21ai_1 _205_ (.B1(_081_),
    .VDD(VDD),
    .Y(_024_),
    .VSS(VSS),
    .A1(net34),
    .A2(_086_));
 sg13g2_nor2_1 _206_ (.A(_108_),
    .B(_062_),
    .Y(_087_),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_nand2_1 _207_ (.Y(_088_),
    .A(net39),
    .B(net40),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_o21ai_1 _208_ (.B1(_040_),
    .VDD(VDD),
    .Y(_089_),
    .VSS(VSS),
    .A1(net41),
    .A2(_088_));
 sg13g2_a221oi_1 _209_ (.VDD(VDD),
    .VSS(VSS),
    .B2(_082_),
    .C1(_089_),
    .B1(_087_),
    .A1(net12),
    .Y(_090_),
    .A2(_083_));
 sg13g2_o21ai_1 _210_ (.B1(_014_),
    .VDD(VDD),
    .Y(_091_),
    .VSS(VSS),
    .A1(_037_),
    .A2(_090_));
 sg13g2_o21ai_1 _211_ (.B1(_091_),
    .VDD(VDD),
    .Y(_025_),
    .VSS(VSS),
    .A1(net12),
    .A2(_066_));
 sg13g2_nand2_1 _212_ (.Y(_092_),
    .A(_008_),
    .B(_065_),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_nand3_1 _213_ (.B(net41),
    .C(net40),
    .A(net39),
    .Y(_093_),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_nand2b_1 _214_ (.Y(_094_),
    .B(_108_),
    .A_N(_088_),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_o21ai_1 _215_ (.B1(_094_),
    .VDD(VDD),
    .Y(_095_),
    .VSS(VSS),
    .A1(net13),
    .A2(_089_));
 sg13g2_a21oi_1 _216_ (.VSS(VSS),
    .VDD(VDD),
    .A1(_093_),
    .A2(_095_),
    .Y(_096_),
    .B1(_037_));
 sg13g2_o21ai_1 _217_ (.B1(_092_),
    .VDD(VDD),
    .Y(_026_),
    .VSS(VSS),
    .A1(net34),
    .A2(_096_));
 sg13g2_a21oi_1 _218_ (.VSS(VSS),
    .VDD(VDD),
    .A1(_052_),
    .A2(_064_),
    .Y(_097_),
    .B1(_093_));
 sg13g2_nor2_1 _219_ (.A(_009_),
    .B(_097_),
    .Y(_098_),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_a221oi_1 _220_ (.VDD(VDD),
    .VSS(VSS),
    .B2(cmp_q),
    .C1(_098_),
    .B1(_097_),
    .A1(_043_),
    .Y(_027_),
    .A2(_066_));
 sg13g2_a22oi_1 _221_ (.Y(_028_),
    .B1(_064_),
    .B2(_109_),
    .A2(_049_),
    .A1(_048_),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_nand2_1 _222_ (.Y(_099_),
    .A(net25),
    .B(net36),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_o21ai_1 _223_ (.B1(_099_),
    .VDD(VDD),
    .Y(_029_),
    .VSS(VSS),
    .A1(_108_),
    .A2(net36));
 sg13g2_nand2_1 _224_ (.Y(_100_),
    .A(net26),
    .B(net35),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_o21ai_1 _225_ (.B1(_100_),
    .VDD(VDD),
    .Y(_030_),
    .VSS(VSS),
    .A1(_003_),
    .A2(net35));
 sg13g2_nand2_1 _226_ (.Y(_101_),
    .A(net27),
    .B(net35),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_o21ai_1 _227_ (.B1(_101_),
    .VDD(VDD),
    .Y(_031_),
    .VSS(VSS),
    .A1(_004_),
    .A2(net35));
 sg13g2_nand2_1 _228_ (.Y(_102_),
    .A(net28),
    .B(net36),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_o21ai_1 _229_ (.B1(_102_),
    .VDD(VDD),
    .Y(_032_),
    .VSS(VSS),
    .A1(_005_),
    .A2(net36));
 sg13g2_nand2_1 _230_ (.Y(_103_),
    .A(net29),
    .B(net36),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_o21ai_1 _231_ (.B1(_103_),
    .VDD(VDD),
    .Y(_033_),
    .VSS(VSS),
    .A1(_006_),
    .A2(net36));
 sg13g2_nand2_1 _232_ (.Y(_104_),
    .A(net30),
    .B(net37),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_o21ai_1 _233_ (.B1(_104_),
    .VDD(VDD),
    .Y(_034_),
    .VSS(VSS),
    .A1(_007_),
    .A2(net37));
 sg13g2_nand2_1 _234_ (.Y(_105_),
    .A(net31),
    .B(net35),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_o21ai_1 _235_ (.B1(_105_),
    .VDD(VDD),
    .Y(_035_),
    .VSS(VSS),
    .A1(_008_),
    .A2(net36));
 sg13g2_inv_1 _236__48 (.VDD(VDD),
    .Y(net48),
    .A(clknet_2_2__leaf_clk),
    .VSS(VSS));
 sg13g2_dfrbpq_1 _237_ (.RESET_B(net45),
    .VSS(VSS),
    .VDD(VDD),
    .D(_020_),
    .Q(_002_),
    .CLK(clknet_2_2__leaf_clk));
 sg13g2_dfrbpq_1 _238_ (.RESET_B(net45),
    .VSS(VSS),
    .VDD(VDD),
    .D(_021_),
    .Q(_003_),
    .CLK(clknet_2_2__leaf_clk));
 sg13g2_dfrbpq_1 _239_ (.RESET_B(net44),
    .VSS(VSS),
    .VDD(VDD),
    .D(_022_),
    .Q(_004_),
    .CLK(clknet_2_0__leaf_clk));
 sg13g2_dfrbpq_1 _240_ (.RESET_B(net44),
    .VSS(VSS),
    .VDD(VDD),
    .D(_023_),
    .Q(_005_),
    .CLK(clknet_2_1__leaf_clk));
 sg13g2_dfrbpq_1 _241_ (.RESET_B(net44),
    .VSS(VSS),
    .VDD(VDD),
    .D(_024_),
    .Q(_006_),
    .CLK(clknet_2_1__leaf_clk));
 sg13g2_dfrbpq_1 _242_ (.RESET_B(net43),
    .VSS(VSS),
    .VDD(VDD),
    .D(_025_),
    .Q(_007_),
    .CLK(clknet_2_1__leaf_clk));
 sg13g2_dfrbpq_1 _243_ (.RESET_B(net44),
    .VSS(VSS),
    .VDD(VDD),
    .D(_026_),
    .Q(_008_),
    .CLK(clknet_2_0__leaf_clk));
 sg13g2_dfrbpq_1 _244_ (.RESET_B(net45),
    .VSS(VSS),
    .VDD(VDD),
    .D(_027_),
    .Q(_009_),
    .CLK(clknet_2_2__leaf_clk));
 sg13g2_dfrbpq_1 _245_ (.RESET_B(net45),
    .VSS(VSS),
    .VDD(VDD),
    .D(_028_),
    .Q(net5),
    .CLK(clknet_2_2__leaf_clk));
 sg13g2_dfrbpq_1 _246_ (.RESET_B(net44),
    .VSS(VSS),
    .VDD(VDD),
    .D(_029_),
    .Q(net25),
    .CLK(clknet_2_0__leaf_clk));
 sg13g2_dfrbpq_1 _247_ (.RESET_B(net43),
    .VSS(VSS),
    .VDD(VDD),
    .D(_030_),
    .Q(net26),
    .CLK(clknet_2_0__leaf_clk));
 sg13g2_dfrbpq_1 _248_ (.RESET_B(net43),
    .VSS(VSS),
    .VDD(VDD),
    .D(_031_),
    .Q(net27),
    .CLK(clknet_2_0__leaf_clk));
 sg13g2_dfrbpq_1 _249_ (.RESET_B(net43),
    .VSS(VSS),
    .VDD(VDD),
    .D(_032_),
    .Q(net28),
    .CLK(clknet_2_1__leaf_clk));
 sg13g2_dfrbpq_1 _250_ (.RESET_B(net43),
    .VSS(VSS),
    .VDD(VDD),
    .D(_033_),
    .Q(net29),
    .CLK(clknet_2_1__leaf_clk));
 sg13g2_dfrbpq_1 _251_ (.RESET_B(net44),
    .VSS(VSS),
    .VDD(VDD),
    .D(_034_),
    .Q(net30),
    .CLK(clknet_2_1__leaf_clk));
 sg13g2_dfrbpq_1 _252_ (.RESET_B(net43),
    .VSS(VSS),
    .VDD(VDD),
    .D(_035_),
    .Q(net31),
    .CLK(clknet_2_1__leaf_clk));
 sg13g2_dfrbpq_1 _253_ (.RESET_B(net43),
    .VSS(VSS),
    .VDD(VDD),
    .D(_011_),
    .Q(net32),
    .CLK(clknet_2_0__leaf_clk));
 sg13g2_dfrbpq_1 _254_ (.RESET_B(net45),
    .VSS(VSS),
    .VDD(VDD),
    .D(_012_),
    .Q(\state[0] ),
    .CLK(clknet_2_3__leaf_clk));
 sg13g2_dfrbpq_1 _255_ (.RESET_B(net46),
    .VSS(VSS),
    .VDD(VDD),
    .D(_013_),
    .Q(\state[1] ),
    .CLK(clknet_2_3__leaf_clk));
 sg13g2_dfrbpq_1 _256_ (.RESET_B(net46),
    .VSS(VSS),
    .VDD(VDD),
    .D(_014_),
    .Q(\state[2] ),
    .CLK(clknet_2_3__leaf_clk));
 sg13g2_dfrbpq_1 _257_ (.RESET_B(net46),
    .VSS(VSS),
    .VDD(VDD),
    .D(_015_),
    .Q(sample_p),
    .CLK(clknet_2_3__leaf_clk));
 sg13g2_dfrbpq_1 _258_ (.RESET_B(net46),
    .VSS(VSS),
    .VDD(VDD),
    .D(_016_),
    .Q(start_q),
    .CLK(clknet_2_2__leaf_clk));
 sg13g2_dfrbpq_1 _259_ (.RESET_B(net45),
    .VSS(VSS),
    .VDD(VDD),
    .D(_017_),
    .Q(\bit_idx[0] ),
    .CLK(clknet_2_3__leaf_clk));
 sg13g2_dfrbpq_1 _260_ (.RESET_B(net45),
    .VSS(VSS),
    .VDD(VDD),
    .D(_018_),
    .Q(\bit_idx[1] ),
    .CLK(clknet_2_3__leaf_clk));
 sg13g2_dfrbpq_1 _261_ (.RESET_B(net45),
    .VSS(VSS),
    .VDD(VDD),
    .D(_019_),
    .Q(\bit_idx[2] ),
    .CLK(clknet_2_3__leaf_clk));
 sg13g2_dfrbpq_1 _262_ (.RESET_B(net43),
    .VSS(VSS),
    .VDD(VDD),
    .D(_000_),
    .Q(net23),
    .CLK(clknet_2_0__leaf_clk));
 sg13g2_dfrbpq_1 _263_ (.RESET_B(net46),
    .VSS(VSS),
    .VDD(VDD),
    .D(_001_),
    .Q(last_n),
    .CLK(net48));
 sg13g2_buf_16 clkbuf_0_clk (.X(clknet_0_clk),
    .A(clk),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_16 clkbuf_2_0__f_clk (.X(clknet_2_0__leaf_clk),
    .A(clknet_0_clk),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_16 clkbuf_2_1__f_clk (.X(clknet_2_1__leaf_clk),
    .A(clknet_0_clk),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_16 clkbuf_2_2__f_clk (.X(clknet_2_2__leaf_clk),
    .A(clknet_0_clk),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_16 clkbuf_2_3__f_clk (.X(clknet_2_3__leaf_clk),
    .A(clknet_0_clk),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_inv_1 clkload0 (.VDD(VDD),
    .A(clknet_2_0__leaf_clk),
    .VSS(VSS));
 sg13g2_inv_1 clkload1 (.VDD(VDD),
    .A(clknet_2_1__leaf_clk),
    .VSS(VSS));
 sg13g2_inv_1 clkload2 (.VDD(VDD),
    .A(clknet_2_3__leaf_clk),
    .VSS(VSS));
 sg13g2_buf_1 fanout34 (.A(_052_),
    .X(net34),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 fanout35 (.A(net36),
    .X(net35),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 fanout36 (.A(net37),
    .X(net36),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 fanout37 (.A(_041_),
    .X(net37),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 fanout38 (.A(net24),
    .X(net38),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 fanout39 (.A(\bit_idx[2] ),
    .X(net39),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 fanout40 (.A(\bit_idx[1] ),
    .X(net40),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 fanout41 (.A(\bit_idx[0] ),
    .X(net41),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 fanout42 (.A(\state[2] ),
    .X(net42),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 fanout43 (.A(net44),
    .X(net43),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 fanout44 (.A(net3),
    .X(net44),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 fanout45 (.A(net3),
    .X(net45),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 fanout46 (.A(net3),
    .X(net46),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 input1 (.A(cmp),
    .X(net1),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 input2 (.A(cmp_n),
    .X(net2),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 input3 (.A(rst_n),
    .X(net3),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 input4 (.A(start),
    .X(net4),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 output10 (.A(net10),
    .X(dac_code[3]),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 output11 (.A(net11),
    .X(dac_code[4]),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 output12 (.A(net12),
    .X(dac_code[5]),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 output13 (.A(net13),
    .X(dac_code[6]),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 output14 (.A(net14),
    .X(dac_code[7]),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 output15 (.A(net15),
    .X(dac_code_n[0]),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 output16 (.A(net16),
    .X(dac_code_n[1]),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 output17 (.A(net17),
    .X(dac_code_n[2]),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 output18 (.A(net18),
    .X(dac_code_n[3]),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 output19 (.A(net19),
    .X(dac_code_n[4]),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 output20 (.A(net20),
    .X(dac_code_n[5]),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 output21 (.A(net21),
    .X(dac_code_n[6]),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 output22 (.A(net22),
    .X(dac_code_n[7]),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 output23 (.A(net23),
    .X(done),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 output24 (.A(net24),
    .X(hold),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 output25 (.A(net25),
    .X(result[0]),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 output26 (.A(net26),
    .X(result[1]),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 output27 (.A(net27),
    .X(result[2]),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 output28 (.A(net28),
    .X(result[3]),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 output29 (.A(net29),
    .X(result[4]),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 output30 (.A(net30),
    .X(result[5]),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 output31 (.A(net31),
    .X(result[6]),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 output32 (.A(net32),
    .X(result[7]),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 output33 (.A(net33),
    .X(sample),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 output5 (.A(net5),
    .X(busy),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 output6 (.A(net47),
    .X(clk_cmp),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 output7 (.A(net7),
    .X(dac_code[0]),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 output8 (.A(net8),
    .X(dac_code[1]),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 output9 (.A(net9),
    .X(dac_code[2]),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_nand2_1 u_sr_q (.Y(cmp_q),
    .A(net2),
    .B(cmp_qb),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_nand2_1 u_sr_qb (.Y(cmp_qb),
    .A(net1),
    .B(cmp_q),
    .VDD(VDD),
    .VSS(VSS));
endmodule
