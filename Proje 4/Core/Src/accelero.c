/* BEGIN Header */
/**
  ******************************************************************************
  * @file    accelero.c
  * @brief   Accelerometer operations.
  ******************************************************************************
  * @attention
  *
  * Copyright (c) 2023 Tubitak BILGEM.
  * All rights reserved.
  *
  * This software is licensed under terms that can be found in the LICENSE file
  * in the root directory of this software component.
  * If no LICENSE file comes with this software, it is provided AS-IS.
  *
  ******************************************************************************
  */
/* END Header */

/* Includes ------------------------------------------------------------------*/
#include "main.h"
#include "accelero.h"

/* Private typedef -----------------------------------------------------------*/

/* Private define ------------------------------------------------------------*/

/* Private macro -------------------------------------------------------------*/

/* Private variables ---------------------------------------------------------*/
static ACCELERO_Message_t accelero;
static ACCELERO_CTRL_REG1_t ctrl_reg1;
static uint8_t u8X,u8Y,u8Z;

/* Private function prototypes -----------------------------------------------*/

/* External variables --------------------------------------------------------*/
extern SPI_HandleTypeDef hspi1;
extern UART_HandleTypeDef huart2;

extern PCD_HandleTypeDef hpcd_USB_OTG_FS;
/******************************************************************************/
/*           				  Accelero Functions	  				          */
/******************************************************************************/

/**
  * @brief This function initialize Accerelerometer.
  */

void vAccelero_Init(void){
	ctrl_reg1.u8DR = CTRL_REG1_DR_100HZ;
	ctrl_reg1.u8PD = CTRL_REG1_PD_ACTIVE_MODE;
	ctrl_reg1.u8FS = CTRL_REG1_FS_2G;
	ctrl_reg1.u8STP_STM = CTRL_REG1_STP_STM_NORMAL_MODE;
	ctrl_reg1.u8Zen = CTRL_REG1_ZEN_ENABLED;
	ctrl_reg1.u8Yen = CTRL_REG1_YEN_ENABLED;
	ctrl_reg1.u8Xen = CTRL_REG1_XEN_ENABLED;
	uint8_t u8Data;
	vMemcpy(&u8Data,&ctrl_reg1);
	vAccelero_Write(SPI_ADDR_CONTROL_REG_1, u8Data);
	//vAccelero_Write(SPI_ADDR_CONTROL_REG_1, SPI_ADDR_INIT_CONF);
}

/**
  * @brief This function read Accerelerometer data from spesific address.
  */

void vMemcpy(uint8_t *u8Data, ACCELERO_CTRL_REG1_t *ctrl_reg1){
	*u8Data = (ctrl_reg1->u8DR << 7) | (ctrl_reg1->u8PD << 6) | (ctrl_reg1->u8FS << 5) | \
			(ctrl_reg1->u8STP_STM << 3) | (ctrl_reg1->u8Zen << 2) | (ctrl_reg1->u8Yen << 1) | \
			(ctrl_reg1->u8Xen << 0);
}

/**
  * @brief This function read Accerelerometer data from spesific address.
  */

uint8_t u8Accelero_Read(uint8_t u8Addr){
	accelero.u8Address = u8Addr | SPI_READ;
	accelero.u8Data = 0x00;

	HAL_GPIO_WritePin(CS_I2C_SPI_GPIO_Port, CS_I2C_SPI_Pin, GPIO_PIN_RESET);

	HAL_SPI_Transmit(&hspi1, &(accelero.u8Address), 1, 100);
	HAL_SPI_Receive(&hspi1, &(accelero.u8Data), 1, 100);

	HAL_GPIO_WritePin(CS_I2C_SPI_GPIO_Port, CS_I2C_SPI_Pin, GPIO_PIN_SET);
	return accelero.u8Data;
}

/**
  * @brief This function write Accerelerometer data to spesific address.
  */

void vAccelero_Write(uint8_t u8Addr, uint8_t u8Data){
	accelero.u8Address = u8Addr;
	accelero.u8Address = accelero.u8Address & SPI_WRITE;
	accelero.u8Data = u8Data;

	HAL_GPIO_WritePin(CS_I2C_SPI_GPIO_Port, CS_I2C_SPI_Pin, GPIO_PIN_RESET);

	HAL_SPI_Transmit(&hspi1, &(accelero.u8Address), 1, 100);
	HAL_SPI_Transmit(&hspi1, &(accelero.u8Data), 1, 100);

	HAL_GPIO_WritePin(CS_I2C_SPI_GPIO_Port, CS_I2C_SPI_Pin, GPIO_PIN_SET);
}

/**
  * @brief This function initialize Queue struct.
  */

void vAccelero_GetXYZ(void){
	char cBuffer[100] = {0};

	uint8_t u8Temp = u8Accelero_Read(SPI_ADDR_STATUS_REG);

	if((u8Temp & 0x08) != 0x00){
		u8X = u8Accelero_Read(SPI_ADDR_OUTX);
		u8Y = u8Accelero_Read(SPI_ADDR_OUTY);
		u8Z = u8Accelero_Read(SPI_ADDR_OUTZ);

		sprintf(cBuffer,"{\"X\":%u,\"Y\":%u,\"Z\":%u}\r\n",u8X,u8Y,u8Z);

		CDC_Transmit_FS((uint8_t*)cBuffer, strlen(cBuffer));
		HAL_Delay(200);
	}
}
