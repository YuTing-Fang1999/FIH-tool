/* Copyright Statement:
 *
 * This software/firmware and related documentation ("MediaTek Software") are
 * protected under relevant copyright laws. The information contained herein
 * is confidential and proprietary to MediaTek Inc. and/or its licensors.
 * Without the prior written permission of MediaTek inc. and/or its licensors,
 * any reproduction, modification, use or disclosure of MediaTek Software,
 * and information contained herein, in whole or in part, shall be strictly prohibited.
 */
/* MediaTek Inc. (C) 2019. All rights reserved.
 *
 * BY OPENING THIS FILE, RECEIVER HEREBY UNEQUIVOCALLY ACKNOWLEDGES AND AGREES
 * THAT THE SOFTWARE/FIRMWARE AND ITS DOCUMENTATIONS ("MEDIATEK SOFTWARE")
 * RECEIVED FROM MEDIATEK AND/OR ITS REPRESENTATIVES ARE PROVIDED TO RECEIVER ON
 * AN "AS-IS" BASIS ONLY. MEDIATEK EXPRESSLY DISCLAIMS ANY AND ALL WARRANTIES,
 * EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF
 * MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE OR NONINFRINGEMENT.
 * NEITHER DOES MEDIATEK PROVIDE ANY WARRANTY WHATSOEVER WITH RESPECT TO THE
 * SOFTWARE OF ANY THIRD PARTY WHICH MAY BE USED BY, INCORPORATED IN, OR
 * SUPPLIED WITH THE MEDIATEK SOFTWARE, AND RECEIVER AGREES TO LOOK ONLY TO SUCH
 * THIRD PARTY FOR ANY WARRANTY CLAIM RELATING THERETO. RECEIVER EXPRESSLY ACKNOWLEDGES
 * THAT IT IS RECEIVER'S SOLE RESPONSIBILITY TO OBTAIN FROM ANY THIRD PARTY ALL PROPER LICENSES
 * CONTAINED IN MEDIATEK SOFTWARE. MEDIATEK SHALL ALSO NOT BE RESPONSIBLE FOR ANY MEDIATEK
 * SOFTWARE RELEASES MADE TO RECEIVER'S SPECIFICATION OR TO CONFORM TO A PARTICULAR
 * STANDARD OR OPEN FORUM. RECEIVER'S SOLE AND EXCLUSIVE REMEDY AND MEDIATEK'S ENTIRE AND
 * CUMULATIVE LIABILITY WITH RESPECT TO THE MEDIATEK SOFTWARE RELEASED HEREUNDER WILL BE,
 * AT MEDIATEK'S OPTION, TO REVISE OR REPLACE THE MEDIATEK SOFTWARE AT ISSUE,
 * OR REFUND ANY SOFTWARE LICENSE FEES OR SERVICE CHARGE PAID BY RECEIVER TO
 * MEDIATEK FOR SUCH MEDIATEK SOFTWARE AT ISSUE.
 *
 * The following software/firmware and/or related documentation ("MediaTek Software")
 * have been modified by MediaTek Inc. All revisions are subject to any receiver's
 * applicable license agreements with MediaTek Inc.
 */

/********************************************************************************************
 *     LEGAL DISCLAIMER
 *
 *     (Header of MediaTek Software/Firmware Release or Documentation)
 *
 *     BY OPENING OR USING THIS FILE, BUYER HEREBY UNEQUIVOCALLY ACKNOWLEDGES AND AGREES
 *     THAT THE SOFTWARE/FIRMWARE AND ITS DOCUMENTATIONS ("MEDIATEK SOFTWARE") RECEIVED
 *     FROM MEDIATEK AND/OR ITS REPRESENTATIVES ARE PROVIDED TO BUYER ON AN "AS-IS" BASIS
 *     ONLY. MEDIATEK EXPRESSLY DISCLAIMS ANY AND ALL WARRANTIES, EXPRESS OR IMPLIED,
 *     INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR
 *     A PARTICULAR PURPOSE OR NONINFRINGEMENT. NEITHER DOES MEDIATEK PROVIDE ANY WARRANTY
 *     WHATSOEVER WITH RESPECT TO THE SOFTWARE OF ANY THIRD PARTY WHICH MAY BE USED BY,
 *     INCORPORATED IN, OR SUPPLIED WITH THE MEDIATEK SOFTWARE, AND BUYER AGREES TO LOOK
 *     ONLY TO SUCH THIRD PARTY FOR ANY WARRANTY CLAIM RELATING THERETO. MEDIATEK SHALL ALSO
 *     NOT BE RESPONSIBLE FOR ANY MEDIATEK SOFTWARE RELEASES MADE TO BUYER'S SPECIFICATION
 *     OR TO CONFORM TO A PARTICULAR STANDARD OR OPEN FORUM.
 *
 *     BUYER'S SOLE AND EXCLUSIVE REMEDY AND MEDIATEK'S ENTIRE AND CUMULATIVE LIABILITY WITH
 *     RESPECT TO THE MEDIATEK SOFTWARE RELEASED HEREUNDER WILL BE, AT MEDIATEK'S OPTION,
 *     TO REVISE OR REPLACE THE MEDIATEK SOFTWARE AT ISSUE, OR REFUND ANY SOFTWARE LICENSE
 *     FEES OR SERVICE CHARGE PAID BY BUYER TO MEDIATEK FOR SUCH MEDIATEK SOFTWARE AT ISSUE.
 *
 *     THE TRANSACTION CONTEMPLATED HEREUNDER SHALL BE CONSTRUED IN ACCORDANCE WITH THE LAWS
 *     OF THE STATE OF CALIFORNIA, USA, EXCLUDING ITS CONFLICT OF LAWS PRINCIPLES.
 ************************************************************************************************/
#include "camera_custom_nvram.h"
#include "camera_custom_isp_nvram.h"

#include "inc.h"

#define LCE_BASE                                                     LCE_TONE_BASE
#define GMA_BASE                                                     GMA_TONE_BASE
#define DCE_BASE                                                     DCE_TONE_BASE
#define LTM_BASE                                                     LTM_TONE_BASE
#define HLR_BASE                                                     HLR_TONE_BASE
#define GMA_R3_BASE                                                  GMA_R3_TONE_BASE

const ISP_NVRAM_LCE_TUNING_PARAM_T LCE_BASE[1] = {
    // IDX_0
    {
    .rAutoLCEParam = {
        .rLCEBasic = {

            {  30,  50,  80, 120 },  // base strength LV (base10)
            { 230, 250, 315, 315 },  // dark strength base ratio
            { 400, 400, 475, 475 },  // bright strength base ratio

           //  LV0    LV1    LV2    LV3    LV4    LV5    LV6    LV7    LV8    LV9   LV10   LV11   LV12   LV13   LV14   LV15   LV16   LV17   LV18
            { 1450,  1600,  1650,  1700,  2100,  2100,  2100,  2100,  2100,  2100,  2100,  2150,  2150,  2150,  2150,  2150,  2150,  2150,  2150 }, // LVTarget
            {  200,   240,   350,   430,   450,   450,   450,   450,   450,   512,   512,   512,   512,   512,   512,   512,   512,   512,   512 }, // MaxLceGain
            { 2100,  2200,  2300,  2400,  2500,  2600,  2600,  2600,  2600,  2600,  2600,  2600,  2600,  2600,  2600,  2600,  2600,  2600,  2600 }  // MaxFinalTarget
        },

        .rLCEStats = {
            20,     //HistCCLB
            1600,   //HistCCUB
            500,    //GCEratio
            1000,   //i4TCPLB
            20000,  //I4TCPUB
            0,      //Reserve
            20,     //i4DetailRangeRatio --> base 1000
            64,     //i4CenSlopeMin

            600,    //DR_Low_Y_Ratio
            800,    //DR_High_Y_Ratio
            1,      //DR_CompEnable
            800,    //DR_Comp_Y_High_Ratio
            2000,   //DR_Diff_Maximum
            1000,   //DR_Diff_Minimum
            500,    //DR_Flat_Ratio_High_Bound

            1,      //multi-slope enable
            32,     //SlopePoint0
            64,     //SlopePoint1
            128,    //SlopePoint2
            256,    //SlopePoint3
            512,    //SlopePoint4
            51,     //SlopeLow (256 base)

            1536,  //SlopeHigh0 (256 base)
            1536,  //SlopeHigh1
            1536,  //SlopeHigh2
            1280,  //SlopeHigh3
            1024,  //SlopeHigh4

            500,  //dr base
            1,    //lcesho enable
            0,    //lcesho mode (0: 8dir, 1: 4dir)

            0,   //reserve0
            0,   //reserve1
            0,   //reserve2
            0,   //reserve3
            0,   //reserve4
            0,   //reserve5
            0,   //reserve6
            0,   //reserve7

        },

        .rLCELUTs = {//i4LCETbl

            {//  /*                                                Dark    Strength                                               */
             //   LV0   LV1   LV2   LV3   LV4   LV5   LV6   LV7   LV8   LV9   LV10  LV11  LV12  LV13  LV14  LV15  LV16  LV17  LV18
                { 200,  256,  256,  256,  256,  256,  256,  256,  256,  256,  320,  320,  320,  320,  320,  320,  320,  320,  320 },   //  0 DR index
                { 256,  256,  384,  384,  384,  384,  384,  384,  384,  384,  384,  384,  384,  384,  384,  384,  384,  384,  384 },   //  1
                { 384,  384,  384,  384,  384,  384,  384,  384,  384,  384,  384,  384,  384,  384,  384,  384,  384,  384,  384 },   //  2
                { 448,  448,  448,  448,  448,  448,  448,  448,  448,  448,  448,  448,  448,  448,  448,  448,  448,  448,  448 },   //  3
                { 448,  448,  448,  448,  448,  448,  448,  448,  448,  448,  512,  512,  512,  512,  512,  512,  512,  512,  512 },   //  4
                { 448,  448,  448,  448,  448,  448,  448,  448,  448,  448,  512,  512,  512,  512,  512,  512,  512,  512,  512 },   //  5
                { 448,  448,  448,  448,  448,  448,  448,  448,  448,  448,  512,  512,  512,  512,  512,  512,  512,  512,  512 },   //  6
                { 448,  448,  448,  448,  448,  448,  448,  448,  448,  448,  512,  512,  512,  512,  512,  512,  512,  512,  512 },   //  7
                { 512,  512,  512,  512,  512,  512,  512,  512,  512,  512,  576,  512,  512,  512,  512,  512,  512,  512,  512 },   //  8
                { 512,  512,  512,  512,  512,  512,  512,  576,  576,  576,  576,  512,  512,  512,  512,  512,  512,  512,  512 },   //  9
                { 512,  512,  512,  512,  512,  512,  512,  576,  576,  576,  576,  512,  512,  512,  512,  512,  512,  512,  512 }    // 10
            },

            {//  /*                                                Bright    Strength                                               */
             //   LV0   LV1   LV2   LV3   LV4   LV5   LV6   LV7   LV8   LV9   LV10  LV11  LV12  LV13  LV14  LV15  LV16  LV17  LV18
                { 128,  128,  128,  128,  128,  128,  128,  128,  128,  128,  128,  128,  128,  128,  128,  128,  128,  128,  128 },   //  0 DR index
                { 256,  256,  256,  256,  256,  256,  256,  256,  256,  256,  256,  256,  256,  256,  256,  256,  256,  256,  256 },   //  1
                { 384,  384,  384,  384,  384,  384,  384,  384,  384,  384,  384,  384,  384,  384,  384,  384,  384,  384,  384 },   //  2
                { 512,  512,  512,  512,  512,  512,  512,  512,  512,  512,  512,  512,  512,  512,  512,  512,  512,  512,  512 },   //  3
                { 512,  512,  512,  512,  512,  512,  512,  512,  512,  512,  512,  512,  512,  512,  512,  512,  512,  512,  512 },   //  4
                { 512,  512,  512,  512,  512,  512,  512,  512,  512,  512,  512,  512,  512,  512,  512,  512,  512,  512,  512 },   //  5
                { 512,  512,  512,  512,  512,  512,  512,  512,  512,  512,  512,  512,  512,  512,  512,  512,  512,  512,  512 },   //  6
                { 512,  512,  512,  512,  512,  512,  512,  512,  512,  512,  512,  512,  512,  512,  512,  512,  512,  512,  512 },   //  7
                { 512,  512,  512,  512,  512,  512,  512,  512,  512,  512,  512,  512,  512,  512,  512,  512,  512,  512,  512 },   //  8
                { 512,  512,  512,  512,  512,  512,  512,  512,  512,  512,  512,  512,  512,  512,  512,  512,  512,  512,  512 },   //  9
                { 512,  512,  512,  512,  512,  512,  512,  512,  512,  512,  512,  512,  512,  512,  512,  512,  512,  512,  512 }    // 10
            },

            { //i4CenSlopeEnhance
              //  0   1   2   3   4   5   6   7   8   9   10   11
                  0,  3,  5, 10, 12, 16, 12, 10,  5,  3,   0,   0
            }

        },

        .rLCEPara = {
            5,    // FlatAreaPercentage
            400,  // FlatRatioTH
            0,    // dark sky protection enable
            300,  // dark sky percentage
            1700, // dark y low bound
            2000, // dark y high bound
            30,   // dark sky lv low bound
            60,   // dark sky lv high bound
            0,   //reserve
            0,   //reserve
            0,   //reserve
            0,   //reserve
            0,   //reserve
            0,    // enable compensate lce gain
            0,   //reserve
            0,   //reserve
            0,   //reserve
            0,   //reserve

            //{//  LV0    LV1    LV2    LV3    LV4    LV5    LV6    LV7    LV8    LV9   LV10   LV11   LV12   LV13   LV14   LV15   LV16   LV17   LV18
                {   50,    50,    50,    50,    50,    50,    60,    60,    70,    90,   100,   110,   110,   110,   110,   110,   120,   130,   140 }, // 0 LVBriRatio
                {  170,   140,   140,   387,   387,   387,   485,   542,   542,   679,   679,   679,   679,   679,   679,   679,   679,   679,   679 }, // 1 LVBriLimit
                {  141,   141,   141,   141,   141,   141,   141,   141,   141,   141,   141,   141,   141,   141,   141,   141,   141,   141,   141 }, // 2 FlatLumaLoBound
                {  679,   679,   679,   679,   679,   679,   679,   679,   679,   679,   679,   679,   679,   679,   679,   679,   679,   679,   679 }, // 3 FlatLumaHiBound
                {    0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0 }, // 4 i4LCEParaTbl0
                {    0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0 }, // 5 i4LCEParaTbl1
                {    0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0 }, // 6 i4LCEParaTbl2
                {    0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0,     0 } // 7 i4LCEParaTbl3
            //}
        },

        .rFaceLCE = {    //i4FaceLCEPara
            1,    //LCE_FD_Enable
            128,  //LoBoundGainRatio
            128,  //HiBoundGainRatio
            1600,   //DarkFaceLimit
            3000,  //FrontLightTH_L
            3360, //FrontLightTH_H
		    1,    //Face SlopeCtrl Enable
            1536, //SlopeHigh0      -> 6*256 normal max (256-based)
            1536, //SlopeHigh1      -> 6*256 normal max (256-based)
            1536, //SlopeHigh2      -> 6*256 normal max (256-based)
            1280, //SlopeHigh3      -> 5*256 normal max (256-based)
            1024, //SlopeHigh4      -> 4*256 normal max (256-based)
            102,  //SlopeLow        -> 0.4*256 normal min (256-based)
            512,  //FaceSlopeHigh   -> 2.0*256 face max (256-based)
            205,  //FaceSlopeLow    -> 0.8*256 face min (256-based)
            500,  //FaceSlopIntpRat -> slope intp ratio (1000-based)
            800,  //Dark face range (1000-based)
            71,   //FDWidthCropRat (100-based)
            70,   //FDHeightCropRat (100-based)
            0,    //reserve0
            0,    //reserve1
            0,    //reserve2
            0,    //reserve3
            0,    //reserve4
            0,  //reserve5 //Final Bright Slope Min -> 0.4*256 (256-based)
            0,  //reserve6 //Final Dark Slope Min   -> 0.4*256 (256-based)
            0,  //reserve7 //DR Low Perc (1000-based)
            0,  //reserve8 //DR High Perc (1000-based)
            0,  //reserve9 //Face Bright Perc (1000-based)
                  //LV0  LV2   LV4   LV6   LV8   LV10  LV12  LV14  LV16   LV0  LV2   LV4   LV6   LV8   LV10  LV12  LV14  LV16  rsv
            {        0,    0,    0,    0,    0,    0,    0,    0,    0,  105,  105,  105,  105,  105,  105,  105,  105,  105,    0 },   //  i4LCEfaceTbl0  // Bright blend ratio, 1000 based // BrightTH by LV
            {        0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0 },   //  i4LCEfaceTbl1  // Dark linear ratio, 1000 based
                  //LV0  LV1   LV2   LV3   LV4   LV5   LV6   LV7   LV8   LV9  LV10  LV11  LV12  LV13  LV14  LV15  LV16  LV17  LV18
            {        0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0 },   //  i4LCEfaceTbl2  // Gain Diff Low
            {        0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0 },   //  i4LCEfaceTbl3  // Gain Diff High
            {        0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0 },   //  i4LCEfaceTbl4  // Blend Low
            {        0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0 },   //  i4LCEfaceTbl5  // Blend High
            {        0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0 },   //  i4LCEfaceTbl6  // Face DR Low
            {        0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0 },   //  i4LCEfaceTbl7  // Face DR High
            {        0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0 },   //  i4LCEfaceTbl8  // Slope Adjust Low
            {        0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0 },   //  i4LCEfaceTbl9  // Slope Adjust High
            {        0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0 },   //  i4LCEfaceTbl10 // Face Bright Low
            {        0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0 },   //  i4LCEfaceTbl11 // Face Bright High
            {        0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0 },   //  i4LCEfaceTbl12 // Slope Strength Low
            {        0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0 },   //  i4LCEfaceTbl13 // Slope Strength High
            {        0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0 },   //  i4LCEfaceTbl14
            {        0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0 },   //  i4LCEfaceTbl15

            {     //i4CenSlopeEnhance
                  //  0   1   2   3   4   5   6   7   8   9   10   11
                      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,   0,   0
            },
            1,    //bFaceLCESmoothLinkEnable
            0,    //u4RobustFaceSlowSpeedCnt
            20,   //i4RobustFaceSmoothSpeed
            10,   //i4RobustFaceSmoothSlowSpeed
            5,    //i4RobustTargetUpdateFrame
            3,    //u4FaceLCEStableMaxCnt
            0,    //i4FaceLCEInStableThd
            0,    //i4FaceLCEOutStableThd
            0,    //reserve
            0,    //reserve
            0,    //reserve
            0     //reserve
        },

        .rMultiCamSync = {
            0,        // enableSync
            10,       // zoomBase, 1x = 10, 5x = 50, 0.6x = 6
            {         //syncWin[4][4] Record Tele in Wide Window position, and Wide in UltraWide window position.
                { 0, 0, 0, 0},{ 0, 0, 0, 0},{ 0, 0, 0, 0},{ 0, 0, 0, 0}
            },
            { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0} //reserve[10]
        },

        .rLCECustom = {  // rLCECustom
            1,   // calculate lce current gain enable (for 3rd party HDR)
            128, // max_lce_gain_ratio
            30,  //max pline threshold
            0,   //reserve
            0,   //reserve
            0,   //reserve
            0,   //reserve
            0,   //reserve
            0,   //reserve
            0,   //reserve
            0,   //reserve
            0,   //reserve
            0,   //reserve
            0,   //reserve

         // rsv   rsv   rsv   rsv   rsv   rsv   rsv   rsv   rsv   rsv   rsv   rsv   rsv   rsv   rsv   rsv   rsv   rsv   rsv
            { 0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0 },   //  i4ReserveTbl0
            { 0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0 },   //  i4ReserveTbl1
            { 0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0 },   //  i4ReserveTbl2
            { 0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0 },   //  i4ReserveTbl3
        },

        .rLCESmooth = {  // rLCESmooth
            0,        // bSmoothEnable
            70,       // i4LCEPosSpeed
            10,       // i4LCENegSpeed
            10,       // i4LCECrosPosSpeed
            10,       // i4LCECrosNegSpeed
            10,       //i4LCESpeed4AEStable
            10,        //minimum ev step
            0,        //reserve0  min moving step
            0,      //reserve1  ae stable case max step bnd 
            0,        //reserve2      ae stable refined mode
            0,       //reserve3      ae stable refined mode bnd
            0,      //reserve4      ae stable refined mode speed
            0,       //reserve5      ae stable refined mode decreaing ratio
            0,       //reserve6
            0,       //reserve7
            0,        //reserve8
            0,        //reserve9
            0,        //reserve10
            0,        //reserve11
            0,        //reserve12
            0,        //reserve13
            0         //reserve14
            }
        }
    },
};
const ISP_NVRAM_GMA_STRUCT_T GMA_BASE[1] = {
    // IDX_0
    {
      .GGM_Reg = {
		{.set={
        0x00000000, 0x00601806, 0x00C0300C, 0x01104411, 0x01705C17, 0x01C0701C, 0x02208822, 0x0280A028, 0x02F0BC2F, 0x0350D435,
        0x03C0F03C, 0x04210842, 0x04812048, 0x04E1384E, 0x05314C53, 0x05916459, 0x05E1785E, 0x06318C63, 0x0691A469, 0x06E1B86E,
        0x0741D074, 0x0791E479, 0x07F1FC7F, 0x08521485, 0x08A2288A, 0x09024090, 0x09525495, 0x09B26C9B, 0x0A0280A0, 0x0A6298A6,
        0x0AB2ACAB, 0x0B02C0B0, 0x0B52D4B5, 0x0BA2E8BA, 0x0C0300C0, 0x0C5314C5, 0x0CA328CA, 0x0CF33CCF, 0x0D4350D4, 0x0D9364D9,
        0x0DE378DE, 0x0E338CE3, 0x0E83A0E8, 0x0ED3B4ED, 0x0F33CCF3, 0x0F83E0F8, 0x0FD3F4FD, 0x10240902, 0x10741D07, 0x10D4350D,
        0x11244912, 0x11745D17, 0x11C4711C, 0x12148521, 0x12749D27, 0x12C4B12C, 0x1314C531, 0x1364D936, 0x13B4ED3B, 0x14050140,
        0x14551545, 0x14A5294A, 0x14F53D4F, 0x15455154, 0x15956559, 0x16258962, 0x16C5B16C, 0x1755D575, 0x17E5F97E, 0x18761D87,
        0x19064190, 0x19966599, 0x1A2689A2, 0x1AB6ADAB, 0x1B36CDB3, 0x1BC6F1BC, 0x1C4711C4, 0x1CC731CC, 0x1D4751D4, 0x1DC771DC,
        0x1E4791E4, 0x1EB7ADEB, 0x1F37CDF3, 0x1FA7E9FA, 0x20180601, 0x20882208, 0x20F83E0F, 0x21585615, 0x21C8721C, 0x22288A22,
        0x2288A228, 0x22E8BA2E, 0x2348D234, 0x2398E639, 0x23E8FA3E, 0x24491244, 0x24992649, 0x25495254, 0x25E97A5E, 0x2699A669,
        0x2739CE73, 0x27E9FA7E, 0x288A2288, 0x293A4E93, 0x29CA729C, 0x2A6A9AA6, 0x2AFABEAF, 0x2B7ADEB7, 0x2BFAFEBF, 0x2C7B1EC7,
        0x2CEB3ACE, 0x2D5B56D5, 0x2DCB72DC, 0x2E3B8EE3, 0x2EABAAEA, 0x2F1BC6F1, 0x2F8BE2F8, 0x2FFBFEFF, 0x306C1B06, 0x30DC370D,
        0x314C5314, 0x31BC6F1B, 0x322C8B22, 0x32ACAB2A, 0x330CC330, 0x337CDF37, 0x33CCF33C, 0x342D0B42, 0x347D1F47, 0x34CD334C,
        0x350D4350, 0x355D5755, 0x359D6759, 0x35ED7B5E, 0x362D8B62, 0x367D9F67, 0x36BDAF6B, 0x36FDBF6F, 0x374DD374, 0x377DDF77,
        0x37BDEF7B, 0x37EDFB7E, 0x382E0B82, 0x385E1785, 0x388E2388, 0x38BE2F8B, 0x38EE3B8E, 0x392E4B92, 0x395E5795, 0x399E6799,
        0x39CE739C, 0x3A0E83A0, 0x3A3E8FA3, 0x3A6E9BA6, 0x3AAEABAA, 0x3ADEB7AD, 0x3B0EC3B0, 0x3B3ECFB3, 0x3B6EDBB6, 0x3B8EE3B8,
        0x3BBEEFBB, 0x3BDEF7BD, 0x3C0F03C0, 0x3C2F0BC2, 0x3C4F13C4, 0x3C6F1BC6, 0x3C8F23C8, 0x3C9F27C9, 0x3CBF2FCB, 0x3CDF37CD,
        0x3CEF3BCE, 0x3D0F43D0, 0x3D2F4BD2, 0x3D4F53D4, 0x3D6F5BD6, 0x3D9F67D9, 0x3DBF6FDB, 0x3DDF77DD, 0x3E0F83E0, 0x3E2F8BE2,
        0x3E4F93E4, 0x3E6F9BE6, 0x3E8FA3E8, 0x3EAFABEA, 0x3ECFB3EC, 0x3EEFBBEE, 0x3F0FC3F0, 0x3F3FCFF3, 0x3F5FD7F5, 0x3F7FDFF7,
        0x3FAFEBFA, 0x3FCFF3FC
    	}},
        {.set={
        0x00000000, 0x00401004, 0x00802008, 0x00C0300C, 0x01004010, 0x01405014, 0x01806018, 0x01C0701C, 0x02008020, 0x02609826,
        0x02C0B02C, 0x0320C832, 0x0380E038, 0x03E0F83E, 0x04411044, 0x04A1284A, 0x05014050, 0x05816058, 0x06018060, 0x0681A068,
        0x0701C070, 0x0781E078, 0x08020080, 0x08822088, 0x09024090, 0x09625896, 0x09C2709C, 0x0A4290A4, 0x0AC2B0AC, 0x0B22C8B2,
        0x0B82E0B8, 0x0C0300C0, 0x0C8320C8, 0x0CE338CE, 0x0D4350D4, 0x0DC370DC, 0x0E4390E4, 0x0EA3A8EA, 0x0F03C0F0, 0x0F63D8F6,
        0x0FC3F0FC, 0x10240902, 0x10842108, 0x10C4310C, 0x11044110, 0x11645916, 0x11C4711C, 0x12248922, 0x1284A128, 0x12C4B12C,
        0x1304C130, 0x1364D936, 0x13C4F13C, 0x14050140, 0x14451144, 0x14852148, 0x14C5314C, 0x15054150, 0x15455154, 0x15A5695A,
        0x16058160, 0x16459164, 0x1685A168, 0x16C5B16C, 0x1705C170, 0x1785E178, 0x18060180, 0x18862188, 0x19064190, 0x19866198,
        0x1A0681A0, 0x1A86A1A8, 0x1B06C1B0, 0x1B86E1B8, 0x1C0701C0, 0x1C4711C4, 0x1CC731CC, 0x1D4751D4, 0x1DC771DC, 0x1E0781E0,
        0x1E87A1E8, 0x1F07C1F0, 0x1F87E1F8, 0x20080200, 0x20882208, 0x20C8320C, 0x21485214, 0x21886218, 0x21C8721C, 0x22489224,
        0x2288A228, 0x22C8B22C, 0x2308C230, 0x2348D234, 0x23C8F23C, 0x24090240, 0x24491244, 0x24C9324C, 0x25495254, 0x26098260,
        0x2689A268, 0x2709C270, 0x2789E278, 0x280A0280, 0x288A2288, 0x290A4290, 0x298A6298, 0x2A0A82A0, 0x2A8AA2A8, 0x2ACAB2AC,
        0x2B4AD2B4, 0x2B8AE2B8, 0x2C0B02C0, 0x2C4B12C4, 0x2C8B22C8, 0x2D0B42D0, 0x2D4B52D4, 0x2D8B62D8, 0x2DCB72DC, 0x2E4B92E4,
        0x2E8BA2E8, 0x2ECBB2EC, 0x2F4BD2F4, 0x2F8BE2F8, 0x300C0300, 0x304C1304, 0x308C2308, 0x30CC330C, 0x310C4310, 0x314C5314,
        0x318C6318, 0x31CC731C, 0x320C8320, 0x324C9324, 0x328CA328, 0x330CC330, 0x334CD334, 0x338CE338, 0x340D0340, 0x344D1344,
        0x348D2348, 0x34CD334C, 0x350D4350, 0x354D5354, 0x358D6358, 0x35CD735C, 0x360D8360, 0x364D9364, 0x368DA368, 0x36CDB36C,
        0x370DC370, 0x374DD374, 0x378DE378, 0x37CDF37C, 0x380E0380, 0x384E1384, 0x388E2388, 0x38BE2F8B, 0x38DE278D, 0x390E4390,
        0x394E5394, 0x397E5F97, 0x399E6799, 0x39CE739C, 0x3A0E83A0, 0x3A4E93A4, 0x3A8EA3A8, 0x3ACEB3AC, 0x3B0EC3B0, 0x3B4ED3B4,
        0x3B8EE3B8, 0x3BCEF3BC, 0x3C0F03C0, 0x3C3F0FC3, 0x3C5F17C5, 0x3C8F23C8, 0x3CCF33CC, 0x3CFF3FCF, 0x3D1F47D1, 0x3D4F53D4,
        0x3D8F63D8, 0x3DCF73DC, 0x3E0F83E0, 0x3E4F93E4, 0x3E7F9FE7, 0x3E9FA7E9, 0x3EBFAFEB, 0x3EDFB7ED, 0x3F0FC3F0, 0x3F4FD3F4,
        0x3F8FE3F8, 0x3FCFF3FC
    	}},
        {.set={
        0x00000000, 0x00401004, 0x00802008, 0x00C0300C, 0x01004010, 0x01405014, 0x01806018, 0x01C0701C, 0x02008020, 0x02609826,
        0x02C0B02C, 0x0320C832, 0x0380E038, 0x03E0F83E, 0x04411044, 0x04A1284A, 0x05014050, 0x05816058, 0x06018060, 0x0681A068,
        0x0701C070, 0x0781E078, 0x08020080, 0x08822088, 0x09024090, 0x09625896, 0x09C2709C, 0x0A4290A4, 0x0AC2B0AC, 0x0B22C8B2,
        0x0B82E0B8, 0x0C0300C0, 0x0C8320C8, 0x0CE338CE, 0x0D4350D4, 0x0DC370DC, 0x0E4390E4, 0x0EA3A8EA, 0x0F03C0F0, 0x0F63D8F6,
        0x0FC3F0FC, 0x10240902, 0x10842108, 0x10C4310C, 0x11044110, 0x11645916, 0x11C4711C, 0x12248922, 0x1284A128, 0x12C4B12C,
        0x1304C130, 0x1364D936, 0x13C4F13C, 0x14050140, 0x14451144, 0x14852148, 0x14C5314C, 0x15054150, 0x15455154, 0x15A5695A,
        0x16058160, 0x16459164, 0x1685A168, 0x16C5B16C, 0x1705C170, 0x1785E178, 0x18060180, 0x18862188, 0x19064190, 0x19866198,
        0x1A0681A0, 0x1A86A1A8, 0x1B06C1B0, 0x1B86E1B8, 0x1C0701C0, 0x1C4711C4, 0x1CC731CC, 0x1D4751D4, 0x1DC771DC, 0x1E0781E0,
        0x1E87A1E8, 0x1F07C1F0, 0x1F87E1F8, 0x20080200, 0x20882208, 0x20C8320C, 0x21485214, 0x21886218, 0x21C8721C, 0x22489224,
        0x2288A228, 0x22C8B22C, 0x2308C230, 0x2348D234, 0x23C8F23C, 0x24090240, 0x24491244, 0x24C9324C, 0x25495254, 0x26098260,
        0x2689A268, 0x2709C270, 0x2789E278, 0x280A0280, 0x288A2288, 0x290A4290, 0x298A6298, 0x2A0A82A0, 0x2A8AA2A8, 0x2ACAB2AC,
        0x2B4AD2B4, 0x2B8AE2B8, 0x2C0B02C0, 0x2C4B12C4, 0x2C8B22C8, 0x2D0B42D0, 0x2D4B52D4, 0x2D8B62D8, 0x2DCB72DC, 0x2E4B92E4,
        0x2E8BA2E8, 0x2ECBB2EC, 0x2F4BD2F4, 0x2F8BE2F8, 0x300C0300, 0x304C1304, 0x308C2308, 0x30CC330C, 0x310C4310, 0x314C5314,
        0x318C6318, 0x31CC731C, 0x320C8320, 0x324C9324, 0x328CA328, 0x330CC330, 0x334CD334, 0x338CE338, 0x340D0340, 0x344D1344,
        0x348D2348, 0x34CD334C, 0x350D4350, 0x354D5354, 0x358D6358, 0x35CD735C, 0x360D8360, 0x364D9364, 0x368DA368, 0x36CDB36C,
        0x370DC370, 0x374DD374, 0x378DE378, 0x37CDF37C, 0x380E0380, 0x384E1384, 0x388E2388, 0x38BE2F8B, 0x38DE278D, 0x390E4390,
        0x394E5394, 0x397E5F97, 0x399E6799, 0x39CE739C, 0x3A0E83A0, 0x3A4E93A4, 0x3A8EA3A8, 0x3ACEB3AC, 0x3B0EC3B0, 0x3B4ED3B4,
        0x3B8EE3B8, 0x3BCEF3BC, 0x3C0F03C0, 0x3C3F0FC3, 0x3C5F17C5, 0x3C8F23C8, 0x3CCF33CC, 0x3CFF3FCF, 0x3D1F47D1, 0x3D4F53D4,
        0x3D8F63D8, 0x3DCF73DC, 0x3E0F83E0, 0x3E4F93E4, 0x3E7F9FE7, 0x3E9FA7E9, 0x3EBFAFEB, 0x3EDFB7ED, 0x3F0FC3F0, 0x3F4FD3F4,
        0x3F8FE3F8, 0x3FCFF3FC
    	}},
        {.set={
        0x00000000, 0x00A0280A, 0x01405014, 0x01C0701C, 0x02409024, 0x02E0B82E, 0x0380E038, 0x04010040, 0x04812048, 0x05014050,
        0x05816058, 0x05E1785E, 0x06419064, 0x06C1B06C, 0x0741D074, 0x07A1E87A, 0x08020080, 0x08822088, 0x09024090, 0x09625896,
        0x09C2709C, 0x0A4290A4, 0x0AC2B0AC, 0x0B22C8B2, 0x0B82E0B8, 0x0C0300C0, 0x0C8320C8, 0x0CE338CE, 0x0D4350D4, 0x0DC370DC,
        0x0E4390E4, 0x0EA3A8EA, 0x0F03C0F0, 0x0F83E0F8, 0x10040100, 0x10641906, 0x10C4310C, 0x11445114, 0x11C4711C, 0x12248922,
        0x1284A128, 0x12E4B92E, 0x1344D134, 0x13A4E93A, 0x14050140, 0x14651946, 0x14C5314C, 0x15254952, 0x15856158, 0x15E5795E,
        0x16459164, 0x16A5A96A, 0x1705C170, 0x1765D976, 0x17C5F17C, 0x18060180, 0x18461184, 0x18A6298A, 0x19064190, 0x19465194,
        0x19866198, 0x19E6799E, 0x1A4691A4, 0x1A86A1A8, 0x1AC6B1AC, 0x1B46D1B4, 0x1C0701C0, 0x1C8721C8, 0x1D0741D0, 0x1D8761D8,
        0x1E0781E0, 0x1E87A1E8, 0x1F07C1F0, 0x1F87E1F8, 0x20080200, 0x20481204, 0x20C8320C, 0x21485214, 0x21C8721C, 0x22088220,
        0x2288A228, 0x2308C230, 0x2388E238, 0x24090240, 0x24491244, 0x24C9324C, 0x25094250, 0x25495254, 0x25C9725C, 0x26098260,
        0x2689A268, 0x26C9B26C, 0x2709C270, 0x2749D274, 0x2789E278, 0x27C9F27C, 0x280A0280, 0x288A2288, 0x290A4290, 0x298A6298,
        0x2A0A82A0, 0x2A8AA2A8, 0x2B0AC2B0, 0x2B8AE2B8, 0x2C0B02C0, 0x2C8B22C8, 0x2D0B42D0, 0x2D8B62D8, 0x2E0B82E0, 0x2E4B92E4,
        0x2ECBB2EC, 0x2F0BC2F0, 0x2F8BE2F8, 0x2FCBF2FC, 0x300C0300, 0x308C2308, 0x30CC330C, 0x310C4310, 0x314C5314, 0x31CC731C,
        0x320C8320, 0x324C9324, 0x32CCB32C, 0x330CC330, 0x334CD334, 0x338CE338, 0x338CE338, 0x33CCF33C, 0x340D0340, 0x344D1344,
        0x344D1344, 0x348D2348, 0x34CD334C, 0x350D4350, 0x350D4350, 0x354D5354, 0x358D6358, 0x35CD735C, 0x360D8360, 0x364D9364,
        0x368DA368, 0x36CDB36C, 0x36CDB36C, 0x370DC370, 0x374DD374, 0x378DE378, 0x378DE378, 0x37CDF37C, 0x380E0380, 0x384E1384,
        0x384E1384, 0x388E2388, 0x38CE338C, 0x390E4390, 0x390E4390, 0x394E5394, 0x394E5394, 0x398E6398, 0x398E6398, 0x39CE739C,
        0x3A0E83A0, 0x3A4E93A4, 0x3A4E93A4, 0x3A8EA3A8, 0x3A8EA3A8, 0x3ACEB3AC, 0x3ACEB3AC, 0x3B0EC3B0, 0x3B4ED3B4, 0x3B8EE3B8,
        0x3BCEF3BC, 0x3C0F03C0, 0x3C0F03C0, 0x3C4F13C4, 0x3C4F13C4, 0x3C8F23C8, 0x3CCF33CC, 0x3D0F43D0, 0x3D0F43D0, 0x3D4F53D4,
        0x3D4F53D4, 0x3D8F63D8, 0x3D8F63D8, 0x3DCF73DC, 0x3E0F83E0, 0x3E4F93E4, 0x3E8FA3E8, 0x3E8FA3E8, 0x3ECFB3EC, 0x3F0FC3F0,
        0x3F4FD3F4, 0x3F8FE3F8
        }}
      },
      .rGmaParam =  {
         // Normal Preview
           eISP_DYNAMIC_GMA_MODE,  // eGMAMode
           8,                  // i4LowContrastThr
           80,                  // i4LowContrastRatio
           3,                  // i4LowContrastSeg
           {
               {   // i4ContrastWeightingTbl
                   //  0   1   2    3    4    5    6    7    8    9    10
                      50, 80, 100, 100, 100, 100, 100, 100, 100, 100, 100
               },
               {   // i4LVWeightingTbl
                   //LV0   1   2   3   4   5   6   7   8   9   10   11   12   13   14   15   16   17   18   19
                       0,  0,  0,  0,  0,  0,  0,  0, 33, 66, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100
                   //  0,  0,  0,  0,  0, 33, 33, 33, 33, 33,  80,  100, 100, 100, 100, 100, 100, 100, 100, 100
               },
               {   // i4NightContrastWtTbl
                   //  0   1   2    3    4    5    6    7    8    9    10
                    //  50, 50, 50, 50,  50, 30, 20,  15,   0,   0,   0
                 85, 85, 75, 50,  50, 30, 20,  15,   0,   0,   0
               },
               {   // i4NightLVWtTbl
                   //LV0   1    2    3   4   5   6   7   8   9   10   11   12   13   14   15   16   17   18   19
                   //  50,  50,  50,  40, 40, 40, 30, 30,  0,  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  0
                      100, 100, 100, 100, 80, 50, 20, 0,  0,  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  0
               }
           },
           {
               1,      // i4Enable
               0,      // i4WaitAEStable
               10       // i4Speed
           },
           {
               0,      // i4Enable
               51801,  // i4CenterPt
               0,      // i4LowPercent //Enable Dualcam Gamma sync
               100000, // i4LowCurve100
               100000, // i4HighCurve100
               50,     // i4HighPercent
               100,    // i4SlopeH100
               0       // i4SlopeL100
           },
           {
               0       // rGMAFlare.i4Enable
           }
        }
    },
};
const ISP_NVRAM_DCE_TUNING_PARAM_T DCE_BASE[1] = {
    // IDX_0
    {
    .rDceParam =
        0,      //disable DCE
        10,    //smooth speed
        2,      //dce sub-hist num
        950,    //dce_flat_ratio_thd_h
        717,    //dce_flat_ratio_thd_l
        0,      //reserve
        0,      //reserve
        {
                0,      //dce_flat_prot_flag for sub-hist1
                0,      //dce_flat_prot_flag for sub-hist2
                0,      //dce_flat_prot_flag for sub-hist3
                {
                        //LV0   LV1     LV2     LV3     LV4     LV5     LV6     LV7     LV8     LV9     LV10    LV11    LV12    LV13    LV14    LV15    LV16    LV17    LV18   
                        {1100,  1200,   1300,   1600,   1800,   2000,   2000,   2000,   2048,   2200,   2250,   2350,   2350,   2480,   2600,   2700,   2800,   2900,   3096    },//0 slope constrain
                        {0,     0,      0,      0,      0,      0,      0,      0,      0,      0,      0,      0,      0,      0,      0,      0,      0,      0,      0       }, // high bound ratio
                        {0,     0,      0,      0,      0,      0,      0,      0,      0,      0,      0,      0,      0,      0,      0,      0,      0,      0,      0       }, // low bound ratio
                }
        },
        {
                //contrast strength in sub-hist 1
                {
                        //LV0   LV1     LV2     LV3     LV4     LV5     LV6     LV7     LV8     LV9     LV10    LV11    LV12    LV13    LV14    LV15    LV16    LV17    LV18    DR
                        {0,     5,      10,     64,    128,     256,    256,    256,    256,    256,    350,    350,    350,    350,    350,    350,     95,      0,      0}, //0
                        {0,     5,      10,     64,    128,     256,    256,    256,    256,    256,    350,    350,    350,    350,    350,    350,     95,      0,      0}, //1
                        {0,     5,      10,     64,    128,     256,    256,    256,    256,    256,    350,    350,    350,    350,    350,    350,     95,      0,      0}, //2
                        {0,     5,      10,     64,    128,     256,    256,    256,    256,    256,    350,    350,    350,    350,    350,    350,     95,      0,      0}, //3
                        {0,     5,      10,     64,    128,     256,    256,    256,    256,    256,    350,    350,    350,    350,    350,    350,     95,      0,      0}, //4
                        {0,     3,      9,      64,    128,     256,    256,    256,    256,    256,    350,    350,    350,    350,    350,    350,     95,      0,      0}, //5
                        {0,     2,      8,      64,    128,     256,    256,    256,    256,    256,    350,    350,    350,    350,    350,    350,     80,      0,      0}, //6
                        {0,     1,      7,      64,    128,     256,    256,    256,    256,    256,    350,    350,    350,    350,    350,    350,     75,      0,      0}, //7
                        {0,     1,      7,      64,    128,     256,    256,    256,    256,    256,    350,    350,    350,    350,    350,    350,     69,      0,      0}, //8
                        {0,     1,      7,      64,    128,     256,    256,    256,    256,    256,    350,    350,    350,    350,    350,    350,     64,      0,      0}, //9
                        {0,     1,      7,      64,    128,     256,    256,    256,    256,    256,    350,    350,    350,    350,    350,    350,     64,      0,      0}, //10
                },
                //contrast strength in sub-hist 2
                {
                        //LV0   LV1     LV2     LV3     LV4     LV5     LV6     LV7     LV8     LV9     LV10    LV11    LV12    LV13    LV14    LV15    LV16    LV17    LV18    DR
                        {0,     5,      10,     100,    250,    350,    350,    350,    350,    350,    350,    350,    350,    380,    380,    380,     95,      0,      0}, //0
                        {0,     5,      10,     100,    250,    350,    350,    350,    350,    350,    350,    350,    350,    380,    380,    380,     95,      0,      0}, //1
                        {0,     5,      10,     100,    250,    350,    350,    350,    350,    350,    350,    350,    350,    380,    380,    380,     95,      0,      0}, //2
                        {0,     5,      10,     100,    250,    350,    350,    350,    350,    350,    350,    350,    350,    380,    380,    380,     95,      0,      0}, //3
                        {0,     5,      10,     100,    250,    350,    350,    350,    350,    350,    350,    350,    350,    380,    380,    380,     95,      0,      0}, //4
                        {0,     3,      10,     100,    250,    350,    350,    350,    350,    350,    350,    350,    350,    380,    380,    380,     95,      0,      0}, //5
                        {0,     2,      8,      100,    250,    350,    350,    350,    350,    350,    350,    350,    350,    380,    380,    320,     80,      0,      0}, //6
                        {0,     1,      7,      100,    250,    350,    350,    350,    350,    350,    350,    350,    350,    380,    380,    300,     75,      0,      0}, //7
                        {0,     0,      5,      100,    250,    350,    350,    350,    350,    350,    350,    350,    350,    380,    380,    278,     69,      0,      0}, //8
                        {0,     0,      5,      100,    250,    350,    350,    350,    350,    350,    350,    350,    350,    380,    380,    256,     64,      0,      0}, //9
                        {0,     0,      5,      100,    250,    350,    350,    350,    350,    350,    350,    350,    350,    380,    380,    256,     64,      0,      0}, //10
                },
                //contrast strength in sub-hist 3
                {
                        //LV0   LV1     LV2     LV3     LV4     LV5     LV6     LV7     LV8     LV9     LV10    LV11    LV12    LV13    LV14    LV15    LV16    LV17    LV18    DR
                        {0,     5,      10,     100,    250,    350,    350,    350,    350,    350,    700,    700,    700,    700,    700,    700,    175,      0,      0}, //0
                        {0,     5,      10,     100,    250,    350,    350,    350,    350,    350,    700,    700,    700,    700,    700,    700,    175,      0,      0}, //1
                        {0,     5,      10,     100,    250,    350,    350,    350,    350,    350,    700,    700,    700,    700,    700,    700,    175,      0,      0}, //2
                        {0,     5,      10,     100,    250,    350,    350,    350,    350,    350,    700,    700,    700,    700,    700,    700,    175,      0,      0}, //3
                        {0,     5,      10,     100,    250,    350,    350,    350,    350,    350,    700,    700,    700,    700,    700,    700,    175,      0,      0}, //4
                        {0,     3,      10,     100,    250,    350,    350,    350,    350,    350,    700,    700,    700,    700,    700,    700,    175,      0,      0}, //5
                        {0,     2,      8,      100,    250,    350,    350,    350,    350,    350,    700,    700,    700,    700,    700,    700,    175,      0,      0}, //6
                        {0,     1,      7,      100,    250,    350,    350,    350,    350,    350,    700,    700,    700,    700,    700,    700,    175,      0,      0}, //7
                        {0,     0,      5,      100,    250,    350,    350,    350,    350,    350,    700,    700,    700,    700,    700,    700,    175,      0,      0}, //8
                        {0,     0,      5,      100,    250,    350,    350,    350,    350,    350,    700,    700,    700,    700,    700,    700,    175,      0,      0}, //9
                        {0,     0,      5,      100,    250,    350,    350,    350,    350,    350,    700,    700,    700,    700,    700,    700,    175,      0,      0}, //10
                },
                //contrast strength in face
                {
                        //LV0   LV1     LV2     LV3     LV4     LV5     LV6     LV7     LV8     LV9     LV10    LV11    LV12    LV13    LV14    LV15    LV16    LV17    LV18    DR
                        {0,     5,      10,     100,    250,    350,    350,    350,    350,    350,    700,    700,    700,    700,    700,    700,    175,      0,      0}, //0
                        {0,     5,      10,     100,    250,    350,    350,    350,    350,    350,    700,    700,    700,    700,    700,    700,    175,      0,      0}, //1
                        {0,     5,      10,     100,    250,    350,    350,    350,    350,    350,    700,    700,    700,    700,    700,    700,    175,      0,      0}, //2
                        {0,     5,      10,     100,    250,    350,    350,    350,    350,    350,    700,    700,    700,    700,    700,    700,    175,      0,      0}, //3
                        {0,     5,      10,     100,    250,    350,    350,    350,    350,    350,    700,    700,    700,    700,    700,    700,    175,      0,      0}, //4
                        {0,     3,      10,     100,    250,    350,    350,    350,    350,    350,    700,    700,    700,    700,    700,    700,    175,      0,      0}, //5
                        {0,     2,      8,      100,    250,    350,    350,    350,    350,    350,    700,    700,    700,    700,    700,    700,    175,      0,      0}, //6
                        {0,     1,      7,      100,    250,    350,    350,    350,    350,    350,    700,    700,    700,    700,    700,    700,    175,      0,      0}, //7
                        {0,     0,      5,      100,    250,    350,    350,    350,    350,    350,    700,    700,    700,    700,    700,    700,    175,      0,      0}, //8
                        {0,     0,      5,      100,    250,    350,    350,    350,    350,    350,    700,    700,    700,    700,    700,    700,    175,      0,      0}, //9
                        {0,     0,      5,      100,    250,    350,    350,    350,    350,    350,    700,    700,    700,    700,    700,    700,    175,      0,      0}, //10
                }
        },
        {
               0,//dce_rsv0
               1,//dce_rsv1 // dce_face_enable
               5,//dce_rsv2 // dce_face_lv_l
              10,//dce_rsv3 // dce_face_lv_h
             100,//dce_rsv4 // dce_face_dark_blend_ratio_l
             100,//dce_rsv5 // dce_face_dark_blend_ratio_h
             100,//dce_rsv6 // dce_face_middle_blend_ratio_l
             100,//dce_rsv7 // dce_face_middle_blend_ratio_h
              75,//dce_rsv8 // dce_face_bright_blend_ratio_l
               0,//dce_rsv9 // dce_face_bright_blend_ratio_h
               {
                        //LV0   LV1     LV2     LV3     LV4     LV5     LV6     LV7     LV8     LV9     LV10    LV11    LV12    LV13    LV14    LV15    LV16    LV17    LV18   
                        {0,     0,      0,      0,      0,      0,      0,      0,      0,      0,      0,      0,      0,      0,      0,      0,      0,      0,      0    }, //0 slope constrain
                        {0,     0,      0,      0,      0,      0,      0,      0,      0,      0,      0,      0,      0,      0,      0,      0,      0,      0,      0    }, //1
                }
        }
    },
};
const ISP_NVRAM_LTM_TUNING_PARAM_T LTM_BASE[1] = {
    // IDX_0
    {
        .rAutoLTMParam = {
            LTM_MODE_LOCAL,    /* local_tone_mode */
            /* global tone info */
            20210010,    /* clipping_thd_perc */
            500,    /* high_bound_perc */
            /* strut mid_perc_lut */
            {
                1,
                {    1666270268,926366787,1331822592,1464154416,724250681,1146421248,1329541416,606349361,1045233664,1699824700  }
            },
            /* face_protect_param */
            //   face_str_x_low    face_str_x_high    face_str_y_low    face_str_y_high    spf_face_str_x1      spf_face_str_x2       spf_face_str_y1       spf_face_str_y2       reserved    reserved    reserved    reserved    reserved    reserved
            {                0,                60,                0,                75,                  0,                  40,                    0,                   80,                 0,          0,          0,          0,          0,          0 },    /* face_spf_strength */
            0,    /* gct_wt_avg_en */
            10,    /* gct_wt_avg_strength */
            1,    /* gct_stat_source */
            /* spf - avg_d_luma_diff */
            //   LV0     LV2     LV4     LV6     LV8    LV10    LV12     LV0     LV2     LV4     LV6     LV8    LV10    LV12
            {      0,      0,      0,      0,      0,      0,      0,   1000,   1000,   1000,   1000,   1000,   1000,   1000 },    /* avg_d_luma_diff_str */
            {      0,   1100 },    /* ltmso_lct_param */
            /* spf_params */
            {
                //   spf_avg_str  spf_content_diff_param  spf_hw_halo_param   spf_dist_diff_param    reserved    reserved    reserved     reserved   reserved     reserved     reserved     reserved    reserved    reserved
                {              0,                     20,              3000,                   72,          0,           0,          0,           0,         0,           0,           0,           0,          0,          0},    
                /*reserved*/
                {              0,                      0,                 0,                    0,          0,           0,          0,           0,         0,           0,           0,           0,          0,          0}     
            },
            /* struct local_global_blending */
            {
                // face_ref_param
                {      0,     50 },
                {      0,     100 },
                //   LV0     LV1     LV2     LV3     LV4     LV5     LV6     LV7     LV8     LV9    LV10    LV11    LV12    LV13
                {     976168737,522133542,775421952,976168737,522133542,775421952,993077283,555819559,792264704,1077226791,640034604,859635712,757935667,977469440,}
            },
            
            0,    /* manual_curve_mode => 0: free run, 1: LE, 2: SE*/
            1,    /* use_predicted_gct */
            /* spf */
            1,    /* spf_region_en */
            250,  /* ref_min_dr */
            1,    /* glb_ref_en */
            0,    /* glb_blend_ratio */
            /* spf_final_strength */
            //   LV0     LV1     LV2     LV3     LV4    LV5     LV6      LV7     LV8     LV9     LV10    LV11   LV12    LV13
            {    1000,   1000,   1000,   1000,   1000,  1000,   1000,    1000,   1000,   1000,   1000,   1000,  1000,   1000 },  
            /* spf - maj_cont */
            128,    /* glb_smth_param */
            1024,    /* predicted wb gain 1024 based */
            10,    /* lct_perc 1000 based */
            0,    /* maj_cont_dec_rat_high */
            /* lct_multiplier */
            //   LV0      LV1      LV2      LV3      LV4     LV5      LV6       LV7      LV8      LV9      LV10     LV11     LV12     LV13
            {    1200,    1200,    1200,    1200,    1200,    1200,    1200,    1200,    1200,    1200,    1200,    1200,    1200,    1200 },
            /* spatial smooth */
            /* spf */
            1,    /* spatial_smooth_enable */
            /* min_DR, max_DR */
            {     250,  4000 },
            /* lcl_contrast_strength_param  */
            { //LV0     LV1     LV2     LV3     LV4     LV5     LV6     LV7     LV8     LV9     LV10    LV11    LV12    LV13
                {4095,  8190,   10000,  80000,  130000, 130000, 130000, 130000, 130000, 130000, 130000, 130000, 130000, 130000}, // x
                {0   ,  200 ,   300  ,  300  ,  300   , 300   , 300   , 300   , 300   , 300   , 300   , 300   , 300   , 300}    // y
                //{  0   ,    0,      0,       0,       0,      0,      0,      0,      0,      0,      0,      0,      0,      0}    // y
            },
            /* raw_clip_lct_params */
            //   lct_diff_aft_pred_max     lct_diff_aft_pred_min   reserved, reserved
            {                     500,                         0,         0,        0},
            /* dist_slp_constrain_min_bt1 */
            {    250,    250,   350,   350 },
            /* dist_slp_constrain_min_bt2 */
            {    250,    250,   450,   450 },           
            0,        /* oe_bld_ratio */
            /* rcst_blending_wgt and slope ratios*/
            {   //   LV0     LV1     LV2     LV3     LV4     LV5     LV6     LV7     LV8     LV9    LV10    LV11    LV12    LV13
                {      1,      1,      1,      1,      1,      1,      1,      1,      1,      1,      1,      1,      1,      1 },    // blend ratio for full
                {      2,      2,      2,      2,      2,      2,      2,      2,      2,      2,      2,      2,      2,      2 },    // blend ratio for bt
                {      4,      4,      4,      4,      4,      4,      4,      4,      4,      4,      4,      4,      4,      4 },    // blend ratio for bt2                
                { // LV4     LV8     LV10    LV13   
                     100,    100,    100,    100,    /* ratio for dist_slp_constrain_min_full*/
                     100,    100,    100,    100,    /* ratio for dist_slp_constrain_min_bt */
                     100,    100,    100,    100,    /* ratio for dist_slp_constrain_min_bt2 */
                    1000,    200                     /* min_dr_param */
                }
            },
            /* glb_ref_dr_param */
            {   250,   250 },
            /* glb params*/
            {  
                {      0,  500,  1000,   1500,  2000,   2500,   3000,   3500,  /*lnr_wet_lut_x*/    
                       0,    0,     0,      0,     0,      0},                 /*reserved*/
                {   1024,  512,   256,    128,    64,     32,      0,      0,  /*lnr_wet_lut_y*/  
                       0,    0,     0,      0,     0,      0},                 /*reserved*/
                /*lnr_wet_refine_x1   lnr_wet_refine_x2    lnr_wet_refine_y1   lnr_wet_refine_y2*/
                {                50,                150,                1536,               1024,
                /*compress_rate_x1     compress_rate_x2     compress_rate_y1    compress_rate_y2*/
                                250,               1000,                 819,               1126,
                /*ev_dacay_rate*/
                   256,
                /* g1_le_max_protect */      
                     1,   
                /* face_spf_region_en*/
                     1,   
                     0,   0,   0 },    /*reserved*/
                /*glb_ref_dist_param*/
                { 131072, 524288,    300,    100,    500,    200,    500,  900,    0,    0,    0,    0,    0,    0 }
            },
            /* ltm_f2b_distance_reduction_ratio */
            {     10,     12 },
            /* multicamSync */
            {
                0,    /* enableSync */
                10,    /* zoomBase, 1x = 10, 5x = 50, 0.6x = 6 */
                {    /* syncWin[4][4]   Record Tele in Wide Window position, and Wide in UltraWide window position */
                    {      0,      0,      0,      0 },
                    {      0,      0,      0,      0 },
                    {      0,      0,      0,      0 },
                    {      0,      0,      0,      0 }
                }
            },
            /* manual curve */
            /* manual curve enable,  */
                 
            {/*x1, x2, x3*/
                0, 0, 0,      
             /*y1, y2, y3*/    
                0, 0, 0,
                0 /*reserved*/},

            /* reserve - HDR */
            {
                /* spf - d_halo_ind */
                //   LV0     LV2     LV4     LV6     LV8    LV10    LV12     LV0     LV2     LV4     LV6     LV8    LV10    LV12
                {   2000,   2000,   2000,   1000,      0,      0,      0,   4000,   4000,   4000,   2000,    700,   2000,   2000 },    /* d_halo_luma_diff_x */
                {      0,      0,      0,      0,      0,      0,      0,    200,    200,    200,    300,    700,    500,    300 },    /* d_halo_luma_diff_str */
                {     30,     30,     30,     30,     30,     30,     30,    500,    500,    500,    200,    200,    200,    200 },    /* d_halo_cnt_x */
                {    100,    100,    100,    100,    100,    100,    100,    100,    100,    100,    100,    100,    100,    100 },    /* d_halo_cnt_wgt */
                {      0,      0,      0,      0,      0,      0,      0,   1000,   1000,   1000,   1000,   1000,   1000,   1000 },    /* d_halo_ind_x */
                {      0,      0,      0,      0,      0,      0,      0,    200,    200,    300,    800,   1000,   1000,   1000 }     /* d_halo_ind_str */
            },
            /* temporal Smooth */
            /* struct ltms_lock */
            {
                300,
                300,
                0,
                0,
                3,
                0
            },
            /* struct ltm_precheck */
            {
                0,
                0,
                0,
                0,
                0,
                0
            },
            /* struct local_tone_lock */
            {
                300,
                300,
                100,
                100,
                3,
                0
            },
            /* struct smooth_speed */
            {
                100,
                100,
                100,
                100
            },
            /* struct face_smooth_speed */
            {
                100,
                100,
                100,
                100
            },
            10,    /* ct_stable_thd */
            10,    /* tp_stable_thd */
            5,    /* pline_boudary_thd */
            /* pline_delta_ev_speed */
            { 100,    500,   1000 },
            { 100,     35,      0 },
            2,    /* delta_cwr_thsouhld */
            2    /* max_index_count_thsouhld */
        }
    },
};
const ISP_NVRAM_HLR_TUNING_PARAM_T HLR_BASE[1] = {
    // IDX_0
    {
        .rAutoHLRParam={
                //   LV00    LV01    LV02    LV03
                { 0,      30,      85,      120 },  //Not support negative lv
                                                    //   Low  Mid  High
    			{	2200,3400,5800 },
                HLR_MODE_ON,      //HLR_ON_OFF
                {
                    0,
                    1024,
                    2304,
                    3136,
                    3600,
                    3844,
                    3969,
                    4096,
                    18,
    				1,
                    16,
                    16,
                    4,
                    0,
                },
                {
                    //Low CT
                    {   // LV00       LV01       LV02      LV03 
                        { 16,12,2 },{ 16,14,2 },{ 16,16,4 },{ 16,16,4 }
                    },
            //Mid CT
                    {   // LV00       LV01       LV02      LV03
                        { 14,14,2 },{ 14,14,2 },{ 16,16,4 },{ 16,16,4 }
                    },
            //High CT
                    {   // LV00       LV01       LV02      LV03
                        { 14,16,2 },{ 16,16,2 },{ 16,16,4 },{ 16,16,4 }
                    },
                },
            //Reserve
                {
                    { 0,0,0 },{ 0,0,0 },{ 0,0,0 },{ 0,0,0 }
                },
    		    0,//Reserve0
    		    0,//Reserve1
    		    0,//Reserve2
    		    0,//Reserve3
    		    0,//Reserve4
    		    0,//Reserve5
    		    0,//Reserve6   
    		    0,//Reserve7
            }
    },
};
const ISP_NVRAM_GMA_STRUCT_T GMA_R3_BASE[1] = {
    // IDX_0
    {
      .GGM_Reg = {
            {.set={
            0x00000000, 0x00601806, 0x00C0300C, 0x01104411, 0x01705C17, 0x01C0701C, 0x02208822, 0x0280A028, 0x02F0BC2F, 0x0350D435, 
            0x03C0F03C, 0x04210842, 0x04812048, 0x04E1384E, 0x05314C53, 0x05916459, 0x05E1785E, 0x06318C63, 0x0691A469, 0x06E1B86E, 
            0x0741D074, 0x0791E479, 0x07F1FC7F, 0x08521485, 0x08A2288A, 0x09024090, 0x09525495, 0x09B26C9B, 0x0A0280A0, 0x0A6298A6, 
            0x0AB2ACAB, 0x0B02C0B0, 0x0B52D4B5, 0x0BA2E8BA, 0x0C0300C0, 0x0C5314C5, 0x0CA328CA, 0x0CF33CCF, 0x0D4350D4, 0x0D9364D9, 
            0x0DE378DE, 0x0E338CE3, 0x0E83A0E8, 0x0ED3B4ED, 0x0F33CCF3, 0x0F83E0F8, 0x0FD3F4FD, 0x10240902, 0x10741D07, 0x10D4350D, 
            0x11244912, 0x11745D17, 0x11C4711C, 0x12148521, 0x12749D27, 0x12C4B12C, 0x1314C531, 0x1364D936, 0x13B4ED3B, 0x14050140, 
            0x14551545, 0x14A5294A, 0x14F53D4F, 0x15455154, 0x15956559, 0x16258962, 0x16C5B16C, 0x1755D575, 0x17E5F97E, 0x18761D87, 
            0x19064190, 0x19966599, 0x1A2689A2, 0x1AB6ADAB, 0x1B36CDB3, 0x1BC6F1BC, 0x1C4711C4, 0x1CC731CC, 0x1D4751D4, 0x1DC771DC, 
            0x1E4791E4, 0x1EB7ADEB, 0x1F37CDF3, 0x1FA7E9FA, 0x20180601, 0x20882208, 0x20F83E0F, 0x21585615, 0x21C8721C, 0x22288A22, 
            0x2288A228, 0x22E8BA2E, 0x2348D234, 0x2398E639, 0x23E8FA3E, 0x24491244, 0x24992649, 0x25495254, 0x25E97A5E, 0x2699A669, 
            0x2739CE73, 0x27E9FA7E, 0x288A2288, 0x293A4E93, 0x29CA729C, 0x2A6A9AA6, 0x2AFABEAF, 0x2B7ADEB7, 0x2BFAFEBF, 0x2C7B1EC7, 
            0x2CEB3ACE, 0x2D5B56D5, 0x2DCB72DC, 0x2E3B8EE3, 0x2EABAAEA, 0x2F1BC6F1, 0x2F8BE2F8, 0x2FFBFEFF, 0x306C1B06, 0x30DC370D, 
            0x314C5314, 0x31BC6F1B, 0x322C8B22, 0x32ACAB2A, 0x330CC330, 0x337CDF37, 0x33CCF33C, 0x342D0B42, 0x347D1F47, 0x34CD334C, 
            0x350D4350, 0x355D5755, 0x359D6759, 0x35ED7B5E, 0x362D8B62, 0x367D9F67, 0x36BDAF6B, 0x36FDBF6F, 0x374DD374, 0x377DDF77, 
            0x37BDEF7B, 0x37EDFB7E, 0x382E0B82, 0x385E1785, 0x388E2388, 0x38BE2F8B, 0x38EE3B8E, 0x392E4B92, 0x395E5795, 0x399E6799, 
            0x39CE739C, 0x3A0E83A0, 0x3A3E8FA3, 0x3A6E9BA6, 0x3AAEABAA, 0x3ADEB7AD, 0x3B0EC3B0, 0x3B3ECFB3, 0x3B6EDBB6, 0x3B8EE3B8, 
            0x3BBEEFBB, 0x3BDEF7BD, 0x3C0F03C0, 0x3C2F0BC2, 0x3C4F13C4, 0x3C6F1BC6, 0x3C8F23C8, 0x3C9F27C9, 0x3CBF2FCB, 0x3CDF37CD, 
            0x3CEF3BCE, 0x3D0F43D0, 0x3D2F4BD2, 0x3D4F53D4, 0x3D6F5BD6, 0x3D9F67D9, 0x3DBF6FDB, 0x3DDF77DD, 0x3E0F83E0, 0x3E2F8BE2, 
            0x3E4F93E4, 0x3E6F9BE6, 0x3E8FA3E8, 0x3EAFABEA, 0x3ECFB3EC, 0x3EEFBBEE, 0x3F0FC3F0, 0x3F3FCFF3, 0x3F5FD7F5, 0x3F7FDFF7, 
            0x3FAFEBFA, 0x3FCFF3FC
        }},
            {.set={
            0x00000000, 0x00401004, 0x00802008, 0x00C0300C, 0x01004010, 0x01405014, 0x01806018, 0x01C0701C, 0x02008020, 0x02609826,
            0x02C0B02C, 0x0320C832, 0x0380E038, 0x03E0F83E, 0x04411044, 0x04A1284A, 0x05014050, 0x05816058, 0x06018060, 0x0681A068,
            0x0701C070, 0x0781E078, 0x08020080, 0x08822088, 0x09024090, 0x09625896, 0x09C2709C, 0x0A4290A4, 0x0AC2B0AC, 0x0B22C8B2,
            0x0B82E0B8, 0x0C0300C0, 0x0C8320C8, 0x0CE338CE, 0x0D4350D4, 0x0DC370DC, 0x0E4390E4, 0x0EA3A8EA, 0x0F03C0F0, 0x0F63D8F6,
            0x0FC3F0FC, 0x10240902, 0x10842108, 0x10C4310C, 0x11044110, 0x11645916, 0x11C4711C, 0x12248922, 0x1284A128, 0x12C4B12C,
            0x1304C130, 0x1364D936, 0x13C4F13C, 0x14050140, 0x14451144, 0x14852148, 0x14C5314C, 0x15054150, 0x15455154, 0x15A5695A,
            0x16058160, 0x16459164, 0x1685A168, 0x16C5B16C, 0x1705C170, 0x1785E178, 0x18060180, 0x18862188, 0x19064190, 0x19866198,
            0x1A0681A0, 0x1A86A1A8, 0x1B06C1B0, 0x1B86E1B8, 0x1C0701C0, 0x1C4711C4, 0x1CC731CC, 0x1D4751D4, 0x1DC771DC, 0x1E0781E0,
            0x1E87A1E8, 0x1F07C1F0, 0x1F87E1F8, 0x20080200, 0x20882208, 0x20C8320C, 0x21485214, 0x21886218, 0x21C8721C, 0x22489224,
            0x2288A228, 0x22C8B22C, 0x2308C230, 0x2348D234, 0x23C8F23C, 0x24090240, 0x24491244, 0x24C9324C, 0x25495254, 0x26098260,
            0x2689A268, 0x2709C270, 0x2789E278, 0x280A0280, 0x288A2288, 0x290A4290, 0x298A6298, 0x2A0A82A0, 0x2A8AA2A8, 0x2ACAB2AC,
            0x2B4AD2B4, 0x2B8AE2B8, 0x2C0B02C0, 0x2C4B12C4, 0x2C8B22C8, 0x2D0B42D0, 0x2D4B52D4, 0x2D8B62D8, 0x2DCB72DC, 0x2E4B92E4,
            0x2E8BA2E8, 0x2ECBB2EC, 0x2F4BD2F4, 0x2F8BE2F8, 0x300C0300, 0x304C1304, 0x308C2308, 0x30CC330C, 0x310C4310, 0x314C5314,
            0x318C6318, 0x31CC731C, 0x320C8320, 0x324C9324, 0x328CA328, 0x330CC330, 0x334CD334, 0x338CE338, 0x340D0340, 0x344D1344,
            0x348D2348, 0x34CD334C, 0x350D4350, 0x354D5354, 0x358D6358, 0x35CD735C, 0x360D8360, 0x364D9364, 0x368DA368, 0x36CDB36C,
            0x370DC370, 0x374DD374, 0x378DE378, 0x37CDF37C, 0x380E0380, 0x384E1384, 0x388E2388, 0x38CE338C, 0x38CE338C, 0x390E4390,
            0x394E5394, 0x398E6398, 0x398E6398, 0x39CE739C, 0x3A0E83A0, 0x3A4E93A4, 0x3A8EA3A8, 0x3ACEB3AC, 0x3B0EC3B0, 0x3B4ED3B4,
            0x3B8EE3B8, 0x3BCEF3BC, 0x3C0F03C0, 0x3C4F13C4, 0x3C4F13C4, 0x3C8F23C8, 0x3CCF33CC, 0x3D0F43D0, 0x3D0F43D0, 0x3D4F53D4,
            0x3D8F63D8, 0x3DCF73DC, 0x3E0F83E0, 0x3E4F93E4, 0x3E8FA3E8, 0x3E8FA3E8, 0x3ECFB3EC, 0x3ECFB3EC, 0x3F0FC3F0, 0x3F4FD3F4,
            0x3F8FE3F8, 0x3FCFF3FC
        }},
            {.set={
            0x00000000, 0x00401004, 0x00802008, 0x00C0300C, 0x01004010, 0x01405014, 0x01806018, 0x01C0701C, 0x02008020, 0x02609826,
            0x02C0B02C, 0x0320C832, 0x0380E038, 0x03E0F83E, 0x04411044, 0x04A1284A, 0x05014050, 0x05816058, 0x06018060, 0x0681A068,
            0x0701C070, 0x0781E078, 0x08020080, 0x08822088, 0x09024090, 0x09625896, 0x09C2709C, 0x0A4290A4, 0x0AC2B0AC, 0x0B22C8B2,
            0x0B82E0B8, 0x0C0300C0, 0x0C8320C8, 0x0CE338CE, 0x0D4350D4, 0x0DC370DC, 0x0E4390E4, 0x0EA3A8EA, 0x0F03C0F0, 0x0F63D8F6,
            0x0FC3F0FC, 0x10240902, 0x10842108, 0x10C4310C, 0x11044110, 0x11645916, 0x11C4711C, 0x12248922, 0x1284A128, 0x12C4B12C,
            0x1304C130, 0x1364D936, 0x13C4F13C, 0x14050140, 0x14451144, 0x14852148, 0x14C5314C, 0x15054150, 0x15455154, 0x15A5695A,
            0x16058160, 0x16459164, 0x1685A168, 0x16C5B16C, 0x1705C170, 0x1785E178, 0x18060180, 0x18862188, 0x19064190, 0x19866198,
            0x1A0681A0, 0x1A86A1A8, 0x1B06C1B0, 0x1B86E1B8, 0x1C0701C0, 0x1C4711C4, 0x1CC731CC, 0x1D4751D4, 0x1DC771DC, 0x1E0781E0,
            0x1E87A1E8, 0x1F07C1F0, 0x1F87E1F8, 0x20080200, 0x20882208, 0x20C8320C, 0x21485214, 0x21886218, 0x21C8721C, 0x22489224,
            0x2288A228, 0x22C8B22C, 0x2308C230, 0x2348D234, 0x23C8F23C, 0x24090240, 0x24491244, 0x24C9324C, 0x25495254, 0x26098260,
            0x2689A268, 0x2709C270, 0x2789E278, 0x280A0280, 0x288A2288, 0x290A4290, 0x298A6298, 0x2A0A82A0, 0x2A8AA2A8, 0x2ACAB2AC,
            0x2B4AD2B4, 0x2B8AE2B8, 0x2C0B02C0, 0x2C4B12C4, 0x2C8B22C8, 0x2D0B42D0, 0x2D4B52D4, 0x2D8B62D8, 0x2DCB72DC, 0x2E4B92E4,
            0x2E8BA2E8, 0x2ECBB2EC, 0x2F4BD2F4, 0x2F8BE2F8, 0x300C0300, 0x304C1304, 0x308C2308, 0x30CC330C, 0x310C4310, 0x314C5314,
            0x318C6318, 0x31CC731C, 0x320C8320, 0x324C9324, 0x328CA328, 0x330CC330, 0x334CD334, 0x338CE338, 0x340D0340, 0x344D1344,
            0x348D2348, 0x34CD334C, 0x350D4350, 0x354D5354, 0x358D6358, 0x35CD735C, 0x360D8360, 0x364D9364, 0x368DA368, 0x36CDB36C,
            0x370DC370, 0x374DD374, 0x378DE378, 0x37CDF37C, 0x380E0380, 0x384E1384, 0x388E2388, 0x38CE338C, 0x38CE338C, 0x390E4390,
            0x394E5394, 0x398E6398, 0x398E6398, 0x39CE739C, 0x3A0E83A0, 0x3A4E93A4, 0x3A8EA3A8, 0x3ACEB3AC, 0x3B0EC3B0, 0x3B4ED3B4,
            0x3B8EE3B8, 0x3BCEF3BC, 0x3C0F03C0, 0x3C4F13C4, 0x3C4F13C4, 0x3C8F23C8, 0x3CCF33CC, 0x3D0F43D0, 0x3D0F43D0, 0x3D4F53D4,
            0x3D8F63D8, 0x3DCF73DC, 0x3E0F83E0, 0x3E4F93E4, 0x3E8FA3E8, 0x3E8FA3E8, 0x3ECFB3EC, 0x3ECFB3EC, 0x3F0FC3F0, 0x3F4FD3F4,
            0x3F8FE3F8, 0x3FCFF3FC
        }},
            {.set={
    	     0x00000000, 0x00A0280A, 0x01405014, 0x01C0701C, 0x02409024, 0x02E0B82E, 0x0380E038, 0x04010040, 0x04812048, 0x05014050, 
    	     0x05816058, 0x05E1785E, 0x06419064, 0x06C1B06C, 0x0741D074, 0x07A1E87A, 0x08020080, 0x08822088, 0x09024090, 0x09625896, 
    	     0x09C2709C, 0x0A4290A4, 0x0AC2B0AC, 0x0B22C8B2, 0x0B82E0B8, 0x0C0300C0, 0x0C8320C8, 0x0CE338CE, 0x0D4350D4, 0x0DC370DC, 
    	     0x0E4390E4, 0x0EA3A8EA, 0x0F03C0F0, 0x0F83E0F8, 0x10040100, 0x10641906, 0x10C4310C, 0x11445114, 0x11C4711C, 0x12248922, 
    	     0x1284A128, 0x12E4B92E, 0x1344D134, 0x13A4E93A, 0x14050140, 0x14651946, 0x14C5314C, 0x15254952, 0x15856158, 0x15E5795E, 
    	     0x16459164, 0x16A5A96A, 0x1705C170, 0x1765D976, 0x17C5F17C, 0x18060180, 0x18461184, 0x18A6298A, 0x19064190, 0x19465194, 
    	     0x19866198, 0x19E6799E, 0x1A4691A4, 0x1A86A1A8, 0x1AC6B1AC, 0x1B46D1B4, 0x1C0701C0, 0x1C8721C8, 0x1D0741D0, 0x1D8761D8, 
    	     0x1E0781E0, 0x1E87A1E8, 0x1F07C1F0, 0x1F87E1F8, 0x20080200, 0x20481204, 0x20C8320C, 0x21485214, 0x21C8721C, 0x22088220, 
    	     0x2288A228, 0x2308C230, 0x2388E238, 0x24090240, 0x24491244, 0x24C9324C, 0x25094250, 0x25495254, 0x25C9725C, 0x26098260, 
    	     0x2689A268, 0x26C9B26C, 0x2709C270, 0x2749D274, 0x2789E278, 0x27C9F27C, 0x280A0280, 0x288A2288, 0x290A4290, 0x298A6298, 
    	     0x2A0A82A0, 0x2A8AA2A8, 0x2B0AC2B0, 0x2B8AE2B8, 0x2C0B02C0, 0x2C8B22C8, 0x2D0B42D0, 0x2D8B62D8, 0x2E0B82E0, 0x2E4B92E4, 
    	     0x2ECBB2EC, 0x2F0BC2F0, 0x2F8BE2F8, 0x2FCBF2FC, 0x300C0300, 0x308C2308, 0x30CC330C, 0x310C4310, 0x314C5314, 0x31CC731C, 
    	     0x320C8320, 0x324C9324, 0x32CCB32C, 0x330CC330, 0x334CD334, 0x338CE338, 0x338CE338, 0x33CCF33C, 0x340D0340, 0x344D1344, 
    	     0x344D1344, 0x348D2348, 0x34CD334C, 0x350D4350, 0x350D4350, 0x354D5354, 0x358D6358, 0x35CD735C, 0x360D8360, 0x364D9364, 
    	     0x368DA368, 0x36CDB36C, 0x36CDB36C, 0x370DC370, 0x374DD374, 0x378DE378, 0x378DE378, 0x37CDF37C, 0x380E0380, 0x384E1384, 
    	     0x384E1384, 0x388E2388, 0x38CE338C, 0x390E4390, 0x390E4390, 0x394E5394, 0x394E5394, 0x398E6398, 0x398E6398, 0x39CE739C, 
    	     0x3A0E83A0, 0x3A4E93A4, 0x3A4E93A4, 0x3A8EA3A8, 0x3A8EA3A8, 0x3ACEB3AC, 0x3ACEB3AC, 0x3B0EC3B0, 0x3B4ED3B4, 0x3B8EE3B8, 
    	     0x3BCEF3BC, 0x3C0F03C0, 0x3C0F03C0, 0x3C4F13C4, 0x3C4F13C4, 0x3C8F23C8, 0x3CCF33CC, 0x3D0F43D0, 0x3D0F43D0, 0x3D4F53D4, 
    	     0x3D4F53D4, 0x3D8F63D8, 0x3D8F63D8, 0x3DCF73DC, 0x3E0F83E0, 0x3E4F93E4, 0x3E8FA3E8, 0x3E8FA3E8, 0x3ECFB3EC, 0x3F0FC3F0, 
    	     0x3F4FD3F4, 0x3F8FE3F8
        }}
      },
      .rGmaParam =  {
         // Normal Preview
           eISP_DYNAMIC_GMA_MODE,  // eGMAMode
           8,                  // i4LowContrastThr
           80,                  // i4LowContrastRatio
           3,                  // i4LowContrastSeg
           {
               {   // i4ContrastWeightingTbl
                   //  0   1   2    3    4    5    6    7    8    9    10
                      50, 80, 100, 100, 100, 100, 100, 100, 100, 100, 100
               },
               {   // i4LVWeightingTbl
                   //LV0   1   2   3   4   5   6   7   8   9   10   11   12   13   14   15   16   17   18   19
                       0,  0,  0,  0,  0,  0,  0,  0, 33, 66, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100
                   //  0,  0,  0,  0,  0, 33, 33, 33, 33, 33,  80,  100, 100, 100, 100, 100, 100, 100, 100, 100
               },
               {   // i4NightContrastWtTbl
                   //  0   1   2    3    4    5    6    7    8    9    10
                    //  50, 50, 50, 50,  50, 30, 20,  15,   0,   0,   0
                 85, 85, 75, 50,  50, 30, 20,  15,   0,   0,   0
               },
               {   // i4NightLVWtTbl
                   //LV0   1    2    3   4   5   6   7   8   9   10   11   12   13   14   15   16   17   18   19
                   //  50,  50,  50,  40, 40, 40, 30, 30,  0,  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  0
                      100, 100, 100, 100, 80, 50, 20, 0,  0,  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  0
               }
           },
           {
               1,      // i4Enable
               0,      // i4WaitAEStable
               1       // i4Speed
           },
           {
               0,      // i4Enable
               9202,   // i4CenterPt
               50,     // i4LowPercent
               100000, // i4LowCurve100
               100000, // i4HighCurve100
               50,     // i4HighPercent
               100,    // i4SlopeH100
               0     // i4SlopeL100
           },
           {
               0       // rGMAFlare.i4Enable
           }
        }
    },
};
