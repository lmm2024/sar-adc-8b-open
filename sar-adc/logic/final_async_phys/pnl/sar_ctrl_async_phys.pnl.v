module sar_ctrl_async_phys (busy,
    cmp_fault,
    cmp_fire,
    cmp_n,
    cmp_p,
    cmp_valid,
    done,
    hold_req,
    rst_n,
    sample,
    track,
    VDD,
    VSS,
    bit_active,
    dac_code,
    dac_code_n,
    result);
 output busy;
 output cmp_fault;
 output cmp_fire;
 input cmp_n;
 input cmp_p;
 output cmp_valid;
 output done;
 output hold_req;
 input rst_n;
 output sample;
 input track;
 inout VDD;
 inout VSS;
 output [7:0] bit_active;
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
 wire _010_;
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
 wire \active_reg[0] ;
 wire \active_reg[1] ;
 wire \active_reg[2] ;
 wire \active_reg[3] ;
 wire \active_reg[4] ;
 wire \active_reg[5] ;
 wire \active_reg[6] ;
 wire \active_reg[7] ;
 wire net4;
 wire net5;
 wire net6;
 wire net7;
 wire net8;
 wire net9;
 wire net10;
 wire net11;
 wire net12;
 wire cmp_decision_hold;
 wire net13;
 wire net14;
 wire net1;
 wire net2;
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
 wire net25;
 wire net26;
 wire net27;
 wire net28;
 wire net29;
 wire net30;
 wire net31;
 wire decision_hold_reset;
 wire decision_hold_set;
 wire net32;
 wire event_pending;
 wire event_pending_reset;
 wire guard_request;
 wire guard_request_delayed;
 wire guard_reset;
 wire guard_set;
 wire hold_elapsed;
 wire hold_elapsed_tail;
 wire net33;
 wire net34;
 wire net35;
 wire net36;
 wire net37;
 wire net38;
 wire net39;
 wire net40;
 wire net41;
 wire net3;
 wire net42;
 wire sar_event_raw;
 wire settle_ready;
 wire track_n;
 wire \u_decision_hold.q_n ;
 wire \u_event_clock_delay.t0 ;
 wire \u_event_pending.q_n ;
 wire \u_hold_delay.t0 ;
 wire \u_hold_delay.t1 ;
 wire \u_hold_delay.t2 ;
 wire \u_interbit_delay.t0 ;
 wire \u_interbit_delay.t1 ;
 wire \u_launch_width.t0 ;
 wire \u_launch_width.t1 ;
 wire \u_launch_width.t2 ;
 wire \u_settle_latch.q_n ;
 wire net43;
 wire net44;
 wire net45;
 wire net46;
 wire net47;
 wire net48;
 wire net49;
 wire net50;
 wire net51;
 wire net52;
 wire net53;
 wire net54;

 sg13g2_decap_8 FILLER_0_0 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_0_14 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_0_21 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_0_28 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_0_35 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_0_42 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_0_49 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_2 FILLER_0_56 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_0_61 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_0_68 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_0_7 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_10_0 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_10_15 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_10_22 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_10_29 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_10_40 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_10_47 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_4 FILLER_10_54 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_2 FILLER_10_58 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_4 FILLER_10_65 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_2 FILLER_10_69 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_2 FILLER_10_7 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_10_75 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_4 FILLER_10_82 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_1 FILLER_10_9 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_2 FILLER_11_0 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_2 FILLER_11_16 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_1 FILLER_11_2 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_11_23 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_2 FILLER_11_30 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_1 FILLER_11_32 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_11_72 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_11_79 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_11_86 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_4 FILLER_11_93 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_1 FILLER_11_97 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_2 FILLER_12_0 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_1 FILLER_12_113 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_1 FILLER_12_28 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_2 FILLER_12_38 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_1 FILLER_12_40 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_1 FILLER_12_45 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_2 FILLER_12_78 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_1 FILLER_12_80 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_1 FILLER_13_0 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_1 FILLER_13_113 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_2 FILLER_13_37 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_1 FILLER_13_98 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_1 FILLER_14_113 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_14_17 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_2 FILLER_14_24 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_1 FILLER_14_26 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_14_39 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_4 FILLER_14_4 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_14_46 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_14_53 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_4 FILLER_14_60 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_2 FILLER_14_64 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_2 FILLER_14_76 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_15_0 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_15_16 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_15_23 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_4 FILLER_15_30 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_2 FILLER_15_34 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_15_45 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_15_52 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_15_59 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_15_66 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_15_73 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_15_80 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_1 FILLER_15_91 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_2 FILLER_16_0 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_16_15 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_16_22 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_16_29 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_16_36 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_16_43 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_2 FILLER_16_50 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_1 FILLER_16_52 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_16_67 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_1 FILLER_16_79 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_17_11 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_2 FILLER_17_111 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_1 FILLER_17_113 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_17_18 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_17_25 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_17_32 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_1 FILLER_17_39 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_17_4 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_2 FILLER_17_77 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_18_0 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_2 FILLER_18_112 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_18_14 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_18_21 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_18_28 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_18_35 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_18_42 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_4 FILLER_18_49 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_2 FILLER_18_53 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_18_7 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_2 FILLER_18_82 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_1 FILLER_18_84 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_19_0 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_2 FILLER_19_111 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_1 FILLER_19_113 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_19_14 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_19_21 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_19_28 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_19_35 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_19_42 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_19_49 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_2 FILLER_19_56 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_19_7 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_2 FILLER_19_89 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_1 FILLER_19_91 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_1_11 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_1_18 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_1_25 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_1_32 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_1_39 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_1_4 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_2 FILLER_1_46 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_1 FILLER_1_51 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_20_0 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_20_12 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_20_19 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_20_26 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_20_33 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_20_40 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_20_47 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_20_54 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_20_61 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_4 FILLER_20_68 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_1 FILLER_20_7 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_2 FILLER_20_99 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_21_0 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_21_14 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_21_21 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_21_28 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_21_35 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_21_42 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_4 FILLER_21_49 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_1 FILLER_21_53 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_21_7 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_21_81 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_2 FILLER_21_88 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_22_11 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_22_18 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_22_25 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_22_32 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_22_39 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_22_4 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_22_46 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_22_53 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_22_60 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_22_67 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_22_74 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_22_81 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_2 FILLER_22_88 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_2_0 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_2_14 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_2_21 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_2_28 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_2 FILLER_2_35 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_2_7 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_3_0 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_3_14 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_3_21 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_3_28 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_3_35 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_3_42 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_1 FILLER_3_52 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_3_7 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_1 FILLER_3_80 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_4_0 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_4_14 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_4_21 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_4_28 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_4_35 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_4_69 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_4_7 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_4 FILLER_4_76 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_5_11 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_5_18 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_5_25 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_5_32 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_5_39 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_5_4 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_5_46 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_5_53 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_2 FILLER_5_64 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_5_73 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_5_80 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_6_0 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_6_14 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_6_21 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_6_28 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_6_35 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_6_42 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_2 FILLER_6_49 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_1 FILLER_6_51 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_6_7 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_4 FILLER_6_89 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_7_0 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_1 FILLER_7_113 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_7_14 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_1 FILLER_7_21 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_7_40 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_4 FILLER_7_47 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_7_7 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_7_78 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_1 FILLER_7_85 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_8_0 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_2 FILLER_8_111 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_1 FILLER_8_113 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_8_14 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_4 FILLER_8_21 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_8_50 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_4 FILLER_8_57 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_2 FILLER_8_61 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_4 FILLER_8_67 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_8_7 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_1 FILLER_8_71 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_2 FILLER_8_77 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_9_0 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_1 FILLER_9_17 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_9_22 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_1 FILLER_9_29 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_4 FILLER_9_46 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_decap_8 FILLER_9_53 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_2 FILLER_9_60 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_1 FILLER_9_62 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_fill_1 FILLER_9_7 (.VDD(VDD),
    .VSS(VSS));
 sg13g2_inv_1 _056_ (.VDD(VDD),
    .Y(_054_),
    .A(cmp_decision_hold),
    .VSS(VSS));
 sg13g2_inv_1 _057_ (.VDD(VDD),
    .Y(_007_),
    .A(net50),
    .VSS(VSS));
 sg13g2_inv_1 _058_ (.VDD(VDD),
    .Y(_055_),
    .A(guard_request),
    .VSS(VSS));
 sg13g2_inv_1 _059_ (.VDD(VDD),
    .Y(track_n),
    .A(track),
    .VSS(VSS));
 sg13g2_a21oi_1 _060_ (.VSS(VSS),
    .VDD(VDD),
    .A1(_054_),
    .A2(\active_reg[7] ),
    .Y(_033_),
    .B1(_016_));
 sg13g2_nor2_1 _061_ (.A(_007_),
    .B(_033_),
    .Y(_024_),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_and2_1 _062_ (.A(net50),
    .B(\active_reg[7] ),
    .X(net11),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_nor2b_1 _063_ (.A(net45),
    .B_N(net11),
    .Y(_006_),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_nand2b_1 _064_ (.Y(net30),
    .B(net49),
    .A_N(_015_),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_a21oi_1 _065_ (.VSS(VSS),
    .VDD(VDD),
    .A1(_054_),
    .A2(\active_reg[6] ),
    .Y(_034_),
    .B1(net30));
 sg13g2_nor2_1 _066_ (.A(_006_),
    .B(_034_),
    .Y(_023_),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_and2_1 _067_ (.A(\active_reg[6] ),
    .B(net49),
    .X(net10),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_nor2b_1 _068_ (.A(net45),
    .B_N(net10),
    .Y(_005_),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_nand2b_1 _069_ (.Y(net29),
    .B(net48),
    .A_N(_014_),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_a21oi_1 _070_ (.VSS(VSS),
    .VDD(VDD),
    .A1(_054_),
    .A2(\active_reg[5] ),
    .Y(_035_),
    .B1(net29));
 sg13g2_nor2_1 _071_ (.A(_005_),
    .B(_035_),
    .Y(_022_),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_and2_1 _072_ (.A(\active_reg[5] ),
    .B(net50),
    .X(net9),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_nor2b_1 _073_ (.A(net45),
    .B_N(net9),
    .Y(_004_),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_nand2b_1 _074_ (.Y(net28),
    .B(net46),
    .A_N(_013_),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_a21oi_1 _075_ (.VSS(VSS),
    .VDD(VDD),
    .A1(_054_),
    .A2(\active_reg[4] ),
    .Y(_036_),
    .B1(net28));
 sg13g2_nor2_1 _076_ (.A(_004_),
    .B(_036_),
    .Y(_021_),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_and2_1 _077_ (.A(net48),
    .B(\active_reg[4] ),
    .X(net8),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_nor2b_1 _078_ (.A(net45),
    .B_N(net8),
    .Y(_003_),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_nand2b_1 _079_ (.Y(net27),
    .B(net46),
    .A_N(_012_),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_a21oi_1 _080_ (.VSS(VSS),
    .VDD(VDD),
    .A1(_054_),
    .A2(\active_reg[3] ),
    .Y(_037_),
    .B1(net27));
 sg13g2_nor2_1 _081_ (.A(_003_),
    .B(_037_),
    .Y(_020_),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_and2_1 _082_ (.A(net49),
    .B(\active_reg[3] ),
    .X(net7),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_nor2b_1 _083_ (.A(net44),
    .B_N(net7),
    .Y(_002_),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_nand2b_1 _084_ (.Y(net26),
    .B(net46),
    .A_N(_011_),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_a21oi_1 _085_ (.VSS(VSS),
    .VDD(VDD),
    .A1(_054_),
    .A2(\active_reg[2] ),
    .Y(_038_),
    .B1(net26));
 sg13g2_nor2_1 _086_ (.A(_002_),
    .B(_038_),
    .Y(_019_),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_and2_1 _087_ (.A(net49),
    .B(\active_reg[2] ),
    .X(net6),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_nor2b_1 _088_ (.A(net45),
    .B_N(net6),
    .Y(_001_),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_nand2b_1 _089_ (.Y(net25),
    .B(net46),
    .A_N(_010_),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_a21oi_1 _090_ (.VSS(VSS),
    .VDD(VDD),
    .A1(_054_),
    .A2(\active_reg[1] ),
    .Y(_039_),
    .B1(net25));
 sg13g2_nor2_1 _091_ (.A(_001_),
    .B(_039_),
    .Y(_018_),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_and2_1 _092_ (.A(net49),
    .B(\active_reg[1] ),
    .X(net5),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_nor2b_1 _093_ (.A(net45),
    .B_N(net5),
    .Y(_000_),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_nand2b_1 _094_ (.Y(net24),
    .B(net46),
    .A_N(_009_),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_a21oi_1 _095_ (.VSS(VSS),
    .VDD(VDD),
    .A1(_054_),
    .A2(\active_reg[0] ),
    .Y(_040_),
    .B1(net24));
 sg13g2_nor2_1 _096_ (.A(_000_),
    .B(_040_),
    .Y(_017_),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_nor2_1 _097_ (.A(net1),
    .B(net2),
    .Y(net13),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_and2_1 _098_ (.A(net1),
    .B(net2),
    .X(_041_),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_inv_1 _099_ (.VDD(VDD),
    .Y(net15),
    .A(_041_),
    .VSS(VSS));
 sg13g2_o21ai_1 _100_ (.B1(net50),
    .VDD(VDD),
    .Y(_042_),
    .VSS(VSS),
    .A1(net1),
    .A2(net2));
 sg13g2_nor2_1 _101_ (.A(net1),
    .B(_042_),
    .Y(decision_hold_set),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_nor2_1 _102_ (.A(_007_),
    .B(guard_request),
    .Y(_043_),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_and2_1 _103_ (.A(guard_request_delayed),
    .B(_043_),
    .X(guard_set),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_nand3b_1 _104_ (.B(net52),
    .C(net50),
    .Y(decision_hold_reset),
    .VDD(VDD),
    .VSS(VSS),
    .A_N(guard_set));
 sg13g2_nor2_1 _105_ (.A(track),
    .B(hold_elapsed_tail),
    .Y(_044_),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_nand3_1 _106_ (.B(_041_),
    .C(_044_),
    .A(hold_elapsed),
    .Y(_045_),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_o21ai_1 _107_ (.B1(_045_),
    .VDD(VDD),
    .Y(sar_event_raw),
    .VSS(VSS),
    .A1(_041_),
    .A2(_042_));
 sg13g2_o21ai_1 _108_ (.B1(net53),
    .VDD(VDD),
    .Y(event_pending_reset),
    .VSS(VSS),
    .A1(_055_),
    .A2(sar_event_raw));
 sg13g2_nand2_1 _109_ (.Y(guard_reset),
    .A(net52),
    .B(_043_),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_nor2_1 _110_ (.A(net50),
    .B(track_n),
    .Y(net42),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_nand2b_1 _111_ (.Y(_046_),
    .B(settle_ready),
    .A_N(event_pending),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_nor4_1 _112_ (.A(_007_),
    .B(guard_request),
    .C(net15),
    .D(_046_),
    .Y(net14),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_nand2_1 _113_ (.Y(_008_),
    .A(net50),
    .B(net45),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_inv_1 _114_ (.VDD(VDD),
    .Y(net4),
    .A(net43),
    .VSS(VSS));
 sg13g2_nand2_1 _115_ (.Y(net16),
    .A(net47),
    .B(_009_),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_nand2_1 _116_ (.Y(net17),
    .A(net47),
    .B(_010_),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_nand2_1 _117_ (.Y(net18),
    .A(net47),
    .B(_011_),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_nand2_1 _118_ (.Y(net19),
    .A(net46),
    .B(_012_),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_nand2_1 _119_ (.Y(net20),
    .A(net47),
    .B(_013_),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_nand2_1 _120_ (.Y(net21),
    .A(net46),
    .B(_014_),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_nand2_1 _121_ (.Y(net22),
    .A(net49),
    .B(_015_),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_nand2_1 _122_ (.Y(net23),
    .A(net49),
    .B(_016_),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_nand2b_1 _123_ (.Y(net31),
    .B(net46),
    .A_N(_016_),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_a22oi_1 _124_ (.Y(_047_),
    .B1(net43),
    .B2(net34),
    .A2(_040_),
    .A1(net44),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_inv_1 _125_ (.VDD(VDD),
    .Y(_025_),
    .A(_047_),
    .VSS(VSS));
 sg13g2_a22oi_1 _126_ (.Y(_048_),
    .B1(net43),
    .B2(net35),
    .A2(_039_),
    .A1(net44),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_inv_1 _127_ (.VDD(VDD),
    .Y(_026_),
    .A(_048_),
    .VSS(VSS));
 sg13g2_a22oi_1 _128_ (.Y(_049_),
    .B1(net43),
    .B2(net36),
    .A2(_038_),
    .A1(net44),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_inv_1 _129_ (.VDD(VDD),
    .Y(_027_),
    .A(_049_),
    .VSS(VSS));
 sg13g2_a22oi_1 _130_ (.Y(_050_),
    .B1(_008_),
    .B2(net37),
    .A2(_037_),
    .A1(net44),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_inv_1 _131_ (.VDD(VDD),
    .Y(_028_),
    .A(_050_),
    .VSS(VSS));
 sg13g2_a22oi_1 _132_ (.Y(_051_),
    .B1(net43),
    .B2(net38),
    .A2(_036_),
    .A1(net44),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_inv_1 _133_ (.VDD(VDD),
    .Y(_029_),
    .A(_051_),
    .VSS(VSS));
 sg13g2_a22oi_1 _134_ (.Y(_052_),
    .B1(net43),
    .B2(net39),
    .A2(_035_),
    .A1(net44),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_inv_1 _135_ (.VDD(VDD),
    .Y(_030_),
    .A(_052_),
    .VSS(VSS));
 sg13g2_a22oi_1 _136_ (.Y(_053_),
    .B1(net43),
    .B2(net40),
    .A2(_034_),
    .A1(net44),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_inv_1 _137_ (.VDD(VDD),
    .Y(_031_),
    .A(_053_),
    .VSS(VSS));
 sg13g2_mux2_1 _138_ (.A0(net41),
    .A1(_033_),
    .S(net4),
    .X(_032_),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_dfrbpq_1 _139_ (.RESET_B(net51),
    .VSS(VSS),
    .VDD(VDD),
    .D(_025_),
    .Q(net34),
    .CLK(guard_request));
 sg13g2_dfrbpq_1 _140_ (.RESET_B(net51),
    .VSS(VSS),
    .VDD(VDD),
    .D(_026_),
    .Q(net35),
    .CLK(guard_request));
 sg13g2_dfrbpq_1 _141_ (.RESET_B(net51),
    .VSS(VSS),
    .VDD(VDD),
    .D(_027_),
    .Q(net36),
    .CLK(guard_request));
 sg13g2_dfrbpq_1 _142_ (.RESET_B(net51),
    .VSS(VSS),
    .VDD(VDD),
    .D(_028_),
    .Q(net37),
    .CLK(guard_request));
 sg13g2_dfrbpq_1 _143_ (.RESET_B(net51),
    .VSS(VSS),
    .VDD(VDD),
    .D(_029_),
    .Q(net38),
    .CLK(guard_request));
 sg13g2_dfrbpq_1 _144_ (.RESET_B(net51),
    .VSS(VSS),
    .VDD(VDD),
    .D(_030_),
    .Q(net39),
    .CLK(guard_request));
 sg13g2_dfrbpq_1 _145_ (.RESET_B(net51),
    .VSS(VSS),
    .VDD(VDD),
    .D(_031_),
    .Q(net40),
    .CLK(guard_request));
 sg13g2_dfrbpq_1 _146_ (.RESET_B(net51),
    .VSS(VSS),
    .VDD(VDD),
    .D(_032_),
    .Q(net41),
    .CLK(guard_request));
 sg13g2_dfrbpq_1 _147_ (.RESET_B(net52),
    .VSS(VSS),
    .VDD(VDD),
    .D(net43),
    .Q(net12),
    .CLK(guard_request));
 sg13g2_dfrbpq_1 _148_ (.RESET_B(net52),
    .VSS(VSS),
    .VDD(VDD),
    .D(net4),
    .Q(net32),
    .CLK(guard_request));
 sg13g2_dfrbpq_1 _149_ (.RESET_B(net53),
    .VSS(VSS),
    .VDD(VDD),
    .D(_017_),
    .Q(_009_),
    .CLK(guard_request));
 sg13g2_dfrbpq_1 _150_ (.RESET_B(net54),
    .VSS(VSS),
    .VDD(VDD),
    .D(_018_),
    .Q(_010_),
    .CLK(guard_request));
 sg13g2_dfrbpq_1 _151_ (.RESET_B(net54),
    .VSS(VSS),
    .VDD(VDD),
    .D(_019_),
    .Q(_011_),
    .CLK(guard_request));
 sg13g2_dfrbpq_1 _152_ (.RESET_B(net53),
    .VSS(VSS),
    .VDD(VDD),
    .D(_020_),
    .Q(_012_),
    .CLK(guard_request));
 sg13g2_dfrbpq_1 _153_ (.RESET_B(net54),
    .VSS(VSS),
    .VDD(VDD),
    .D(_021_),
    .Q(_013_),
    .CLK(guard_request));
 sg13g2_dfrbpq_1 _154_ (.RESET_B(net54),
    .VSS(VSS),
    .VDD(VDD),
    .D(_022_),
    .Q(_014_),
    .CLK(guard_request));
 sg13g2_dfrbpq_1 _155_ (.RESET_B(net53),
    .VSS(VSS),
    .VDD(VDD),
    .D(_023_),
    .Q(_015_),
    .CLK(guard_request));
 sg13g2_dfrbpq_1 _156_ (.RESET_B(net53),
    .VSS(VSS),
    .VDD(VDD),
    .D(_024_),
    .Q(_016_),
    .CLK(guard_request));
 sg13g2_dfrbpq_1 _157_ (.RESET_B(net52),
    .VSS(VSS),
    .VDD(VDD),
    .D(_000_),
    .Q(\active_reg[0] ),
    .CLK(guard_request));
 sg13g2_dfrbpq_1 _158_ (.RESET_B(net52),
    .VSS(VSS),
    .VDD(VDD),
    .D(_001_),
    .Q(\active_reg[1] ),
    .CLK(guard_request));
 sg13g2_dfrbpq_1 _159_ (.RESET_B(net52),
    .VSS(VSS),
    .VDD(VDD),
    .D(_002_),
    .Q(\active_reg[2] ),
    .CLK(guard_request));
 sg13g2_dfrbpq_1 _160_ (.RESET_B(net53),
    .VSS(VSS),
    .VDD(VDD),
    .D(_003_),
    .Q(\active_reg[3] ),
    .CLK(guard_request));
 sg13g2_dfrbpq_1 _161_ (.RESET_B(net54),
    .VSS(VSS),
    .VDD(VDD),
    .D(_004_),
    .Q(\active_reg[4] ),
    .CLK(guard_request));
 sg13g2_dfrbpq_1 _162_ (.RESET_B(net54),
    .VSS(VSS),
    .VDD(VDD),
    .D(_005_),
    .Q(\active_reg[5] ),
    .CLK(guard_request));
 sg13g2_dfrbpq_1 _163_ (.RESET_B(net53),
    .VSS(VSS),
    .VDD(VDD),
    .D(_006_),
    .Q(\active_reg[6] ),
    .CLK(guard_request));
 sg13g2_dfrbpq_1 _164_ (.RESET_B(net53),
    .VSS(VSS),
    .VDD(VDD),
    .D(_007_),
    .Q(\active_reg[7] ),
    .CLK(guard_request));
 sg13g2_buf_1 _165_ (.A(net50),
    .X(net33),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 fanout43 (.A(_008_),
    .X(net43),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 fanout44 (.A(net45),
    .X(net44),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 fanout45 (.A(\active_reg[0] ),
    .X(net45),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 fanout46 (.A(net48),
    .X(net46),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 fanout47 (.A(net48),
    .X(net47),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 fanout48 (.A(net12),
    .X(net48),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 fanout49 (.A(net12),
    .X(net49),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 fanout50 (.A(net12),
    .X(net50),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 fanout51 (.A(net52),
    .X(net51),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 fanout52 (.A(net3),
    .X(net52),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 fanout53 (.A(net3),
    .X(net53),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 fanout54 (.A(net3),
    .X(net54),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 input1 (.A(cmp_n),
    .X(net1),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 input2 (.A(cmp_p),
    .X(net2),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 input3 (.A(rst_n),
    .X(net3),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 output10 (.A(net10),
    .X(bit_active[6]),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 output11 (.A(net11),
    .X(bit_active[7]),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 output12 (.A(net49),
    .X(busy),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 output13 (.A(net13),
    .X(cmp_fault),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 output14 (.A(net14),
    .X(cmp_fire),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 output15 (.A(net15),
    .X(cmp_valid),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 output16 (.A(net16),
    .X(dac_code[0]),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 output17 (.A(net17),
    .X(dac_code[1]),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 output18 (.A(net18),
    .X(dac_code[2]),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 output19 (.A(net19),
    .X(dac_code[3]),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 output20 (.A(net20),
    .X(dac_code[4]),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 output21 (.A(net21),
    .X(dac_code[5]),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 output22 (.A(net22),
    .X(dac_code[6]),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 output23 (.A(net23),
    .X(dac_code[7]),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 output24 (.A(net24),
    .X(dac_code_n[0]),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 output25 (.A(net25),
    .X(dac_code_n[1]),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 output26 (.A(net26),
    .X(dac_code_n[2]),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 output27 (.A(net27),
    .X(dac_code_n[3]),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 output28 (.A(net28),
    .X(dac_code_n[4]),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 output29 (.A(net29),
    .X(dac_code_n[5]),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 output30 (.A(net30),
    .X(dac_code_n[6]),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 output31 (.A(net31),
    .X(dac_code_n[7]),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 output32 (.A(net32),
    .X(done),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 output33 (.A(net33),
    .X(hold_req),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 output34 (.A(net34),
    .X(result[0]),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 output35 (.A(net35),
    .X(result[1]),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 output36 (.A(net36),
    .X(result[2]),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 output37 (.A(net37),
    .X(result[3]),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 output38 (.A(net38),
    .X(result[4]),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 output39 (.A(net39),
    .X(result[5]),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 output4 (.A(net4),
    .X(bit_active[0]),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 output40 (.A(net40),
    .X(result[6]),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 output41 (.A(net41),
    .X(result[7]),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 output42 (.A(net42),
    .X(sample),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 output5 (.A(net5),
    .X(bit_active[1]),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 output6 (.A(net6),
    .X(bit_active[2]),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 output7 (.A(net7),
    .X(bit_active[3]),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 output8 (.A(net8),
    .X(bit_active[4]),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_buf_1 output9 (.A(net9),
    .X(bit_active[5]),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_nor2_1 \u_decision_hold.u_q  (.A(decision_hold_reset),
    .B(\u_decision_hold.q_n ),
    .Y(cmp_decision_hold),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_nor2_1 \u_decision_hold.u_qn  (.A(decision_hold_set),
    .B(cmp_decision_hold),
    .Y(\u_decision_hold.q_n ),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_dlygate4sd3_1 \u_event_clock_delay.u_d0  (.A(event_pending),
    .VDD(VDD),
    .VSS(VSS),
    .X(\u_event_clock_delay.t0 ));
 sg13g2_dlygate4sd3_1 \u_event_clock_delay.u_d1  (.A(\u_event_clock_delay.t0 ),
    .VDD(VDD),
    .VSS(VSS),
    .X(guard_request));
 sg13g2_nor2_1 \u_event_pending.u_q  (.A(event_pending_reset),
    .B(\u_event_pending.q_n ),
    .Y(event_pending),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_nor2_1 \u_event_pending.u_qn  (.A(sar_event_raw),
    .B(event_pending),
    .Y(\u_event_pending.q_n ),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_dlygate4sd3_1 \u_hold_delay.u_d0  (.A(track_n),
    .VDD(VDD),
    .VSS(VSS),
    .X(\u_hold_delay.t0 ));
 sg13g2_dlygate4sd3_1 \u_hold_delay.u_d1  (.A(\u_hold_delay.t0 ),
    .VDD(VDD),
    .VSS(VSS),
    .X(\u_hold_delay.t1 ));
 sg13g2_dlygate4sd3_1 \u_hold_delay.u_d2  (.A(\u_hold_delay.t1 ),
    .VDD(VDD),
    .VSS(VSS),
    .X(\u_hold_delay.t2 ));
 sg13g2_dlygate4sd3_1 \u_hold_delay.u_d3  (.A(\u_hold_delay.t2 ),
    .VDD(VDD),
    .VSS(VSS),
    .X(hold_elapsed));
 sg13g2_dlygate4sd3_1 \u_interbit_delay.u_d0  (.A(guard_request),
    .VDD(VDD),
    .VSS(VSS),
    .X(\u_interbit_delay.t0 ));
 sg13g2_dlygate4sd3_1 \u_interbit_delay.u_d1  (.A(\u_interbit_delay.t0 ),
    .VDD(VDD),
    .VSS(VSS),
    .X(\u_interbit_delay.t1 ));
 sg13g2_dlygate4sd3_1 \u_interbit_delay.u_d2  (.A(\u_interbit_delay.t1 ),
    .VDD(VDD),
    .VSS(VSS),
    .X(guard_request_delayed));
 sg13g2_dlygate4sd3_1 \u_launch_width.u_d0  (.A(hold_elapsed),
    .VDD(VDD),
    .VSS(VSS),
    .X(\u_launch_width.t0 ));
 sg13g2_dlygate4sd3_1 \u_launch_width.u_d1  (.A(\u_launch_width.t0 ),
    .VDD(VDD),
    .VSS(VSS),
    .X(\u_launch_width.t1 ));
 sg13g2_dlygate4sd3_1 \u_launch_width.u_d2  (.A(\u_launch_width.t1 ),
    .VDD(VDD),
    .VSS(VSS),
    .X(\u_launch_width.t2 ));
 sg13g2_dlygate4sd3_1 \u_launch_width.u_d3  (.A(\u_launch_width.t2 ),
    .VDD(VDD),
    .VSS(VSS),
    .X(hold_elapsed_tail));
 sg13g2_nor2_1 \u_settle_latch.u_q  (.A(guard_reset),
    .B(\u_settle_latch.q_n ),
    .Y(settle_ready),
    .VDD(VDD),
    .VSS(VSS));
 sg13g2_nor2_1 \u_settle_latch.u_qn  (.A(guard_set),
    .B(settle_ready),
    .Y(\u_settle_latch.q_n ),
    .VDD(VDD),
    .VSS(VSS));
endmodule
